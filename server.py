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
            model="llama3-70b-8192",  # 🔥 fast + powerful
            messages=[
                {"role": "system", "content": "You are A+ AI created by Aarush. Be helpful and modern."},
                {"role": "user", "content": user_message}
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
