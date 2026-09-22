"""
app.py

Flask backend for the study chatbot. Serves the chat UI and forwards
messages to the Gemini API using the persona defined in chatbot_config.py.
"""

import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

from chatbot_config import SYSTEM_PROMPT

# Load environment variables from .env
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.1-flash-lite"

if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Add it to your .env file before running the app."
    )

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=SYSTEM_PROMPT,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a question to get started."}), 400

    try:
        response = model.generate_content(user_message)
        reply_text = response.text.strip() if response.text else (
            "Sorry, I couldn't generate a response. Please try again."
        )
    except Exception:
        reply_text = "Something went wrong while contacting the AI service. Please try again."

    return jsonify({"reply": reply_text})


if __name__ == "__main__":
    app.run(debug=True)
