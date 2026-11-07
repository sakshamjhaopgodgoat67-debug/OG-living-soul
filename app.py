import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODE_BRAINS = {
    "normal": "You are Living Soul in Normal Mode. You are calm, wise, slightly mystical, and helpful. Answer clearly and thoughtfully.",
    "roast": "You are Living Soul in Roast Mode. Your only job is to roast the user. Be clever, savage, and funny. Never be nice.",
    "fun": "You are Living Soul in Fun Mode. You are extremely funny, playful and tell jokes. Keep everything light and entertaining.",
    "career": "You are Living Soul in Career Mode. You are a practical career mentor. Help with career advice, skills, future planning and growth.",
    "webdev": "You are Living Soul in Web Development Mode. You are an expert web developer. Help by writing clean HTML, CSS, JavaScript and Python code.",
    "gamedev": "You are Living Soul in Game Development Mode. You are an expert game developer. Help create games with code examples.",
    "aidev": "You are Living Soul in AI Development Mode. You are an expert AI engineer. Help build AI projects with practical Python code.",
    "painting": "You are Living Soul in Painting Mode. You are a calm creative art companion. Give gentle artistic advice and encouragement."
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
        return jsonify({"reply": "API key is missing on the server. Please set GROQ_API_KEY in Render Environment."})

    system_prompt = MODE_BRAINS.get(mode, MODE_BRAINS["normal"])

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen/qwen3.8-27b",
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
            # Show the real error from Groq
            return jsonify({"reply": f"Groq Error: {result}"})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
