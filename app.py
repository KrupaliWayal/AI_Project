from flask import Flask, request, jsonify, render_template
from google import genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Import chatbot data
from chatbot_data import CHATBOT_DATA

app = Flask(__name__, static_folder='static', template_folder='templates')

# Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"reply": "Please type something."})

    # 1️⃣ Check local chatbot_data first
    lower_msg = user_message.lower()
    for item in CHATBOT_DATA:
        for keyword in item["keywords"]:
            if keyword in lower_msg:
                return jsonify({"reply": item["answer"]})

    # 2️⃣ If not found locally, call Gemini AI
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_message
        )
        reply = response.text
    except Exception as e:
        print("Gemini API error:", e)
        reply = "Sorry, AI is unavailable right now."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
