import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

# ------------------ APP SETUP ------------------
app = Flask(__name__)
CORS(app)

# ------------------ CONFIG ------------------
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

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

        system_text = (
            "You are A+ AI, an intelligent assistant created by Aarush Mishra. "
            "Give clear, helpful, and slightly modern responses."
        )

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=system_text + "\nUser: " + user_message
        )

        reply = response.text if response.text else "No response from AI"

        return jsonify({"reply": reply})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    print("🔥 Server starting...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
