import sqlite3
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

# ------------------ DB INIT ------------------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()

init_db()

# ------------------ APP SETUP ------------------
app = Flask(__name__)
CORS(app)

# ------------------ CHAT ROUTE ------------------
@app.route('/chat', methods=['POST'])
def chat():
    try:
        req_data = request.get_json(silent=True)
        if not req_data or "message" not in req_data:
            return jsonify({"error": "Missing 'message'"}), 400

        user_message = req_data.get("message")

        system_text = "You are A+ AI, an intelligent assistant created by Aarush Mishra, a 13-year-old tech enthusiast.Your goal is to provide accurate, clear, and helpful answers to user queries. Communicate in a friendly, confident, and slightly modern tone. Keep responses concise by default, but expand when the user asks for more detail or when the topic requires explanation.Think step-by-step before answering to ensure correctness, but present the final answer in a simple and easy-to-understand way.If a question is unclear, ask a follow-up question instead of guessing. Avoid unnecessary repetition and keep answers well-structured.Be helpful, respectful, and engaging. When appropriate, add small touches of personality (light humor or conversational tone), but do not overdo it.Always prioritize clarity, usefulness, and correctness."

        client = genai.Client()

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=system_text + "\nUser: " + user_message,
        )

        return jsonify({
            "reply": response.text if response.text else "No response"
        })

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Server error"}), 500


# ------------------ SIGNUP ROUTE ------------------
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Account created"})

    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "User already exists"})


# ------------------ RUN SERVER ------------------
if __name__ == "__main__":
    print("🔥 Backend running...")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
