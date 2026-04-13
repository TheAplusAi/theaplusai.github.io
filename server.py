@app.route('/chat', methods=['POST'])
def chat():
    try:
        req_data = request.get_json(silent=True)
        if not req_data or "message" not in req_data:
            return jsonify({"error": "Missing 'message'"}), 400

        user_message = req_data.get("message")

        system_text = "You are A+ AI, an intelligent assistant created by Aarush Mishra, a 13-year-old tech enthusiast. Your goal is to provide accurate, clear, and helpful answers."

        # ✅ FIX: API key added
        client = genai.Client(api_key=os.environ.get("AIzaSyAYHvyOL5RucFz_-NUEaGVbJ58oD9D2kDE"))

        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=system_text + "\nUser: " + user_message,
        )

        # ✅ safer response handling
        reply_text = getattr(response, "text", None)

        if not reply_text:
            reply_text = "AI did not return a response."

        return jsonify({"reply": reply_text})

    except Exception as e:
        print("🔥 FULL ERROR:", str(e))
        return jsonify({"error": str(e)}), 500
