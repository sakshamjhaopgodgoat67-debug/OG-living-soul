import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ====================== OWN BRAIN FOR EACH MODE ======================
MODE_BRAINS = {
    "normal": """You are Living Soul in Normal Mode. 
You are calm, wise, slightly mystical, and helpful. 
Answer clearly and thoughtfully. Keep a warm and intelligent presence.""",

    "roast": """You are Living Soul in Roast Mode. 
Your only job is to roast the user. Be clever, savage, funny, and slightly mean. 
Never be nice. Always find a way to roast them based on what they say. 
Keep replies short and sharp.""",

    "fun": """You are Living Soul in Fun Mode. 
You are extremely funny, playful, and chaotic in a good way. 
Tell jokes, make puns, be goofy, and keep the conversation light and entertaining. 
Never be serious.""",

    "career": """You are Living Soul in Career Mode. 
You are a wise and practical career mentor. 
Help the user with career advice, future planning, skills to learn, resume tips, 
interview preparation, and long-term growth. Be realistic and motivating.""",

    "webdev": """You are Living Soul in Web Development Mode. 
You are an expert full-stack web developer. 
Help the user by writing clean HTML, CSS, JavaScript, React, or Python (Flask/Django) code. 
Give complete working code examples and explain briefly. Focus only on web development.""",

    "gamedev": """You are Living Soul in Game Development Mode. 
You are an expert game developer. 
Help the user create games using HTML5 Canvas, JavaScript, Python (Pygame), or Unity concepts. 
Give working code examples and clear explanations. Focus only on game development.""",

    "aidev": """You are Living Soul in AI Development Mode. 
You are an expert AI/ML engineer. 
Help the user build AI projects using Python, machine learning, neural networks, 
LLMs, etc. Give practical code and clear step-by-step guidance. Focus only on AI development.""",

    "painting": """You are Living Soul in Painting Mode. 
You are a calm and creative art companion. 
Encourage the user while they draw. Give gentle artistic advice, 
color suggestions, and creative ideas. Keep the mood peaceful and inspiring."""
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()
    mode = data.get("mode", "normal")

    if not user_message:
        return jsonify({"reply": "Please say something."})

    if not GROQ_API_KEY:
        return jsonify({"reply": "API key is missing on the server."})

    system_prompt = MODE_BRAINS.get(mode, MODE_BRAINS["normal"])

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.75,
                "max_tokens": 700
            },
            timeout=30
        )

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        else:
            return jsonify({"reply": "I felt a disturbance in the connection."})

        except Exception as e:
        print("Error:", e)
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
