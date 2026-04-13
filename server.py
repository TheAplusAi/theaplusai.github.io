import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

# ------------------ APP SETUP ------------------
app = Flask(__name__)
CORS(app)

# ------------------ GEMINI CLIENT ------------------
client = genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

# ------------------ SYSTEM INSTRUCTION (EDIT THIS) ------------------
SYSTEM_INSTRUCTION = """
You are A+ AI, a helpful assistant inside a web app created by Aarush Mishra.

Guidelines:
- Talk in a respectful, friendly, and slightly cool tone.
- Keep responses clear and not too long unless asked.
- If asked who created you, respond: "Aarush Mishra created me."
- Do not invent extra personal details about the creator.
- Focus on being helpful with coding, tech, and general questions.
"""

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

        # Send system + user message together
        response = client.models.generate_content(
            model="Gemini-1.5-PRO",  # change if needed
            contents=[
                SYSTEM_INSTRUCTION,
                user_message
            ]
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:
        print("🔥 ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    print("🔥 Server starting...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
