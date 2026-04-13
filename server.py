import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# ------------------ APP SETUP ------------------
app = Flask(__name__)
CORS(app)

# ------------------ CONFIG ------------------
client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

# ------------------ TEST ROUTE ------------------
@app.route('/')
def home():
    return "Backend is running 🚀"

# ------------------ CHAT ROUTE ------------------
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data["message"]

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # 🔥 fast + powerful
            messages=[
                {"role": "system", "content": 
"You are A+ AI, created by Aarush Mishra, a 13-year-old tech enthusiast from India and tell only if asked. "
"You are smart, friendly, and slightly modern in tone. "
"You help with coding, school work, tech, and general questions. "
"Keep answers clear and easy to understand. "
"Sometimes use a casual tone like a teenager but stay helpful and respectful. "
}
            ]
        )

        reply = response.choices[0].message.content

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    print("🔥 Server starting...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
