from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Use relative path to frontend folder
frontend_path = os.path.join(os.path.dirname(__file__), "frontend")
app = Flask(__name__, static_folder=frontend_path)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_input = request.json["message"]
        if "messages" not in session:
            session["messages"] = [
                {"role": "system", "content": "You are a helpful assistant that remembers the user's name and other details."}
            ]
        session["messages"].append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=session["messages"]
        )
        bot_reply = response.choices[0].message.content
        session["messages"].append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print("ERROR:", e)
        return jsonify({"reply": "Sorry, an error occurred!"})

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
