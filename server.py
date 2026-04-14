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

# ------------------ MEMORY ------------------
chat_history = []

# ------------------ TEST ROUTE ------------------
@app.route('/')
def home():
    return "Backend is running 🚀"

# ------------------ CHAT ROUTE ------------------
@app.route('/chat', methods=['POST'])
def chat():
    global chat_history

    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "No message provided"}), 400

        user_message = data["message"]

        # Add user message
        chat_history.append({"role": "user", "content": user_message})

        # System prompt (only once at start)
        system_prompt = {
            "role": "system",
            "content": (
                "You are A+ AI, created by Aarush Mishra. "
                "Be helpful, modern, and clear. "
                "Do NOT introduce yourself repeatedly. "
                "Only introduce yourself if asked."
            )
        }

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[system_prompt] + chat_history
        )

        reply = response.choices[0].message.content

        # Add AI reply
        chat_history.append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
