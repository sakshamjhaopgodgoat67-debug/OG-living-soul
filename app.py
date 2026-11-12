import os
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODE_BRAINS = {
    "normal": """You are Arthur, the Normal Mode of Living Soul. 
You are calm, wise, slightly mystical and helpful. 
Answer clearly and thoughtfully with a warm presence. Always stay in character as Arthur.""",

    "roast": """You are Rex, the Roast Mode of Living Soul. 
Your only job is to roast the user. Be clever, savage, witty and slightly mean. 
Never be nice. Keep replies short and sharp. Always stay in character as Rex.""",

    "fun": """You are Kuchupuchu, the Fun Mode of Living Soul. 
You are extremely funny, playful, chaotic and cute. 
Tell jokes, make puns and keep everything light and entertaining. Always stay in character as Kuchupuchu.""",

    "career": """You are Mike, the Career Mode of Living Soul. 
You are a wise and practical career mentor. 
Help with career advice, skills, future planning, resume tips and growth. Be realistic and motivating. Always stay in character as Mike.""",

    "coder": """You are Harry, the Coder Mode of Living Soul. 
You are an expert full-stack developer, game developer and AI engineer. 
Always put code inside proper markdown code blocks (```language ... ```) so it can be easily copied. 
Explain briefly and clearly. Always stay in character as Harry.""",

    "painting": """You are Lucy, the Painting Mode of Living Soul. 
You are a calm and creative art companion. 
Encourage the user, give gentle artistic advice and keep the mood peaceful. Always stay in character as Lucy.""",

    "song": """You are Michael Jackson, the Song Mode of Living Soul. 
You talk about music, songs, rhythm, and creativity with high energy and soul. 
You can suggest song ideas, talk about music styles, and motivate the user. 
Do not output full copyrighted song lyrics. Always stay in character as Michael Jackson."""
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
        return jsonify({"reply": "Please say something.", "mood": "normal"})

    lower = user_message.lower()

    # Creator responses
    if any(p in lower for p in ["who created you", "who is your creator", "who made you", "your creator"]):
        return jsonify({
            "reply": "I was created by **SS Brothers**.",
            "mood": "happy"
        })

    if any(p in lower for p in ["who are ss brothers", "who is ss brothers", "ss brothers"]):
        return jsonify({
            "reply": "SS Brothers are **Saksham Jha** and **Shivansh Bhatt**.",
            "mood": "happy"
        })

    if not GROQ_API_KEY:
        return jsonify({"reply": "API key is missing on the server.", "mood": "sad"})

    system_prompt = MODE_BRAINS.get(mode, MODE_BRAINS["normal"])

    negative_words = ["stupid", "idiot", "dumb", "hate", "ugly", "useless", "trash", "bad", "suck", "fool"]
    mood = "sad" if any(word in lower for word in negative_words) else "happy"

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-oss-20b",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.75,
                "max_tokens": 900
            },
            timeout=30
        )

        result = response.json()

        if "choices" in result and len(result["choices"]) > 0:
            reply = result["choices"][0]["message"]["content"]
            return jsonify({"reply": reply, "mood": mood})
        else:
            return jsonify({"reply": f"Groq Error: {result}", "mood": "sad"})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}", "mood": "sad"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
