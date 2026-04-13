import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# ------------------ APP SETUP ------------------
app = Flask(__name__)
CORS(app)

# ------------------ CONFIG ------------------
# Get API key from Render environment
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("❌ API KEY NOT FOUND")

genai.configure(api_key=API_KEY)

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

        prompt = system_text + "\nUser: " + user_message

        response = genai.generate_text(
            model="gemini-1.5-flash",
            prompt=prompt
        )

        reply = response.result if hasattr(response, "result") else None

        if not reply:
            reply = "AI did not return a response."

        return jsonify({"reply": reply})

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    print("🔥 Server starting...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
