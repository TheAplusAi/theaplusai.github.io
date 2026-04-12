import sqlite3
import os

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

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
# Enable CORS for all domains (restrict this in production)
CORS(app)

try:
        # Safely parse the JSON payload
        req_data = request.get_json(silent=True)
        if not req_data or "message" not in req_data:
            return jsonify({"error": "Missing 'message' in request body"}), 400
            
        user_message = req_data.get("message")
        system_text = "You are A+ AI, created by Aarush Mishra, a 13-year-old tech enthusiast. You are here to assist users with their queries in a friendly and helpful manner. Always provide accurate and concise information, and feel free to ask follow-up questions if you need more details to assist the user better."

        # Send request to local Ollama instance
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": system_text + "\nUser: " + user_message,
                "stream": False
            },
            timeout=120  # Prevent infinite hanging (120 seconds)
        )
        
        # Raise an exception for bad HTTP status codes from Ollama
        response.raise_for_status()

        data = response.json()

        return jsonify({
            "reply": data.get("response", "No response from AI")
        })

    except requests.exceptions.RequestException as e:
        print("Ollama Connection Error:", e)
        return jsonify({"error": "Could not connect to the local AI model. Is Ollama running?"}), 503
        
    except Exception as e:
        print("General Error:", e)
        return jsonify({"error": "Something went wrong on the server"}), 500

if __name__ == "__main__":
    # Changed port to 5000 to avoid conflicting with frontend frameworks like React
    print("🔥 Backend running at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Account created"})

    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "User already exists"})
    
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Account created"})

    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "User already exists"})
