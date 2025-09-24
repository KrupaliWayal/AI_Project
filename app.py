# # app.py
# import os
# import sqlite3
# import json
# from flask import Flask, request, jsonify, render_template, g
# from dotenv import load_dotenv
# import openai
# from chatbot_data import find_faq_answer

# load_dotenv()  # loads .env file if present

# OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
# if not OPENAI_API_KEY:
#     raise RuntimeError("Please set OPENAI_API_KEY environment variable. See README.")
# openai.api_key = OPENAI_API_KEY

# # Optional: external gold rate provider URL (GET returning JSON with 'rate' field)
# GOLD_RATE_API_URL = os.environ.get("GOLD_RATE_API_URL")  # e.g. https://api.example.com/today-gold

# DATABASE = 'leads.db'
# app = Flask(__name__, static_folder="static", template_folder="templates")

# # --- Database helpers ---
# def get_db():
#     db = getattr(g, "_database", None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row
#     return db

# def init_db():
#     con = sqlite3.connect(DATABASE)
#     cur = con.cursor()
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS leads (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         phone TEXT,
#         email TEXT,
#         message TEXT,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     """)
#     con.commit()
#     con.close()

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, "_database", None)
#     if db is not None:
#         db.close()

# # --- Simple gold rate fetcher (uses configured API or returns mock) ---
# import requests
# def fetch_gold_rate():
#     if GOLD_RATE_API_URL:
#         try:
#             r = requests.get(GOLD_RATE_API_URL, timeout=5)
#             r.raise_for_status()
#             data = r.json()
#             # Expecting JSON like {"rate": 5600}
#             if isinstance(data, dict) and ("rate" in data or "price" in data):
#                 rate = data.get("rate", data.get("price"))
#                 return float(rate)
#         except Exception as e:
#             print("Gold API fetch failed:", e)
#     # fallback/mock
#     return 5600.0

# # --- OpenAI helper ---
# def ask_openai(user_text, system_prompt=None):
#     """
#     Send the user_text to OpenAI ChatCompletion.
#     Replace 'gpt-4o-mini' with a model you have access to.
#     """
#     model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")  # change if needed
#     system_prompt = system_prompt or "You are a helpful assistant for a residential/commercial builders company."
#     try:
#         resp = openai.ChatCompletion.create(
#             model=model,
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_text}
#             ],
#             max_tokens=600,
#             temperature=0.2,
#         )
#         # Note: different OpenAI SDK versions may return responses differently.
#         text = resp["choices"][0]["message"]["content"].strip()
#         return text
#     except Exception as e:
#         print("OpenAI error:", e)
#         return "Sorry — I couldn't reach the AI assistant right now."

# # --- Routes ---
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json or {}
#     user_text = (data.get("message") or "").strip()
#     if not user_text:
#         return jsonify({"error": "empty message"}), 400

#     # 1) check FAQ
#     faq_answer, faq_id = find_faq_answer(user_text)
#     if faq_answer:
#         return jsonify({"reply": faq_answer, "source": "faq", "faq_id": faq_id})

#     # 2) check if user asked for gold rate
#     lower = user_text.lower()
#     if "gold" in lower and ("rate" in lower or "price" in lower):
#         rate = fetch_gold_rate()
#         reply = f"Today's gold rate (per gram, approximate) is ₹{rate:.2f}. This may vary by city and purity."
#         return jsonify({"reply": reply, "source": "gold"})

#     # 3) fallback to OpenAI
#     ai_reply = ask_openai(user_text)
#     return jsonify({"reply": ai_reply, "source": "openai"})

# @app.route("/save_lead", methods=["POST"])
# def save_lead():
#     payload = request.json or {}
#     name = payload.get("name", "").strip()
#     phone = payload.get("phone", "").strip()
#     email = payload.get("email", "").strip()
#     message = payload.get("message", "").strip()
#     if not (name and phone):
#         return jsonify({"error": "name and phone are required"}), 400
#     db = get_db()
#     cur = db.cursor()
#     cur.execute("INSERT INTO leads (name, phone, email, message) VALUES (?, ?, ?, ?)",
#                 (name, phone, email, message))
#     db.commit()
#     return jsonify({"status": "ok"})

# if __name__ == "__main__":
#     init_db()
#     app.run(host="0.0.0.0", port=5000, debug=True)


# import os
# import sqlite3
# import json
# import requests
# from flask import Flask, request, jsonify, render_template, g
# from dotenv import load_dotenv
# from chatbot_data import find_faq_answer

# # Gemini API
# from google import genai

# load_dotenv()

# GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# if not GEMINI_API_KEY:
#     raise RuntimeError("Please set GEMINI_API_KEY in .env file")

# # Initialize Gemini client
# os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
# client = genai.Client()

# GOLD_RATE_API_URL = os.environ.get("GOLD_RATE_API_URL")

# DATABASE = 'leads.db'
# app = Flask(__name__, static_folder="static", template_folder="templates")

# # --- Database helpers ---
# def get_db():
#     db = getattr(g, "_database", None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#         db.row_factory = sqlite3.Row
#     return db

# def init_db():
#     con = sqlite3.connect(DATABASE)
#     cur = con.cursor()
#     cur.execute("""
#     CREATE TABLE IF NOT EXISTS leads (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT,
#         phone TEXT,
#         email TEXT,
#         message TEXT,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     )
#     """)
#     con.commit()
#     con.close()

# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, "_database", None)
#     if db is not None:
#         db.close()

# # --- Gold rate ---
# def fetch_gold_rate():
#     if GOLD_RATE_API_URL:
#         try:
#             r = requests.get(GOLD_RATE_API_URL, timeout=5)
#             r.raise_for_status()
#             data = r.json()
#             rate = data.get("rate", data.get("price"))
#             if rate:
#                 return float(rate)
#         except Exception as e:
#             print("Gold API fetch failed:", e)
#     return 5600.0  # mock

# # --- Gemini AI ---
# def ask_gemini(user_text):
#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=user_text
#         )
#         return response.text
#     except Exception as e:
#         print("Gemini API error:", e)
#         return "Sorry, I couldn't reach the AI assistant right now."

# # --- Routes ---
# @app.route("/")
# def index():
#     return render_template("index.html")

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.json or {}
#     user_text = (data.get("message") or "").strip()
#     if not user_text:
#         return jsonify({"error": "empty message"}), 400

#     # 1) FAQ check
#     faq_answer, faq_id = find_faq_answer(user_text)
#     if faq_answer:
#         return jsonify({"reply": faq_answer, "source": "faq", "faq_id": faq_id})

#     # 2) Gold rate check
#     lower = user_text.lower()
#     if "gold" in lower and ("rate" in lower or "price" in lower):
#         rate = fetch_gold_rate()
#         reply = f"Today's gold rate (per gram, approximate) is ₹{rate:.2f}."
#         return jsonify({"reply": reply, "source": "gold"})

#     # 3) Gemini AI
#     ai_reply = ask_gemini(user_text)
#     return jsonify({"reply": ai_reply, "source": "gemini"})

# @app.route("/save_lead", methods=["POST"])
# def save_lead():
#     payload = request.json or {}
#     name = payload.get("name", "").strip()
#     phone = payload.get("phone", "").strip()
#     email = payload.get("email", "").strip()
#     message = payload.get("message", "").strip()
#     if not (name and phone):
#         return jsonify({"error": "name and phone are required"}), 400
#     db = get_db()
#     cur = db.cursor()
#     cur.execute("INSERT INTO leads (name, phone, email, message) VALUES (?, ?, ?, ?)",
#                 (name, phone, email, message))
#     db.commit()
#     return jsonify({"status": "ok"})

# if __name__ == "__main__":
#     init_db()
#     app.run(host="0.0.0.0", port=5000, debug=True)



# from flask import Flask, request, jsonify, render_template
# from google import genai
# from dotenv import load_dotenv
# import os

# app = Flask(__name__, static_folder='static', template_folder='templates')

# load_dotenv()

# # Gemini API client
# client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# @app.route("/")
# def home():
#     return render_template("index.html")  # our chat frontend

# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     message = data.get("message", "")
#     if not message:
#         return jsonify({"reply": "Please type something."})

#     try:
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=message
#         )
#         reply = response.text
#     except Exception as e:
#         print("Gemini API error:", e)
#         reply = "Sorry, AI is unavailable right now."

#     return jsonify({"reply": reply})

# if __name__ == "__main__":
#     app.run(debug=True)


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
