
## 🏗️ Builder Assistant Chatbot

A smart chatbot built for builder companies to answer customer queries.  
It first checks answers from a predefined dataset (`chatbot_data.py`) and, if no match is found, uses **Google Gemini AI** to generate accurate responses.

---
## ✨ Features

- ✅ Predefined FAQs about builder company services (fast response).  
- 🤖 AI-powered answers using **Gemini API** when data is not found locally.  
- 💬 Clean WhatsApp-style chat UI (blue & white theme).  
- 📱 Responsive layout, works on desktop and mobile.  
- 🔐 Secure API key management using `.env` file.  

---
## 📂 Project Structure

Chatbot/

│── app.py # Flask backend

│── chatbot_data.py # Contains predefined Q&A dataset


│── templates/

│ └── index.html # Chat UI (frontend)

│── static/

│ ├── style.css # Chat UI styling

│ └── main.js # Handles frontend chat logic

│── requirements.txt # Python dependencies

│── .gitignore # Ignore .env and unnecessary files

│── README.md # Project documentation


---
## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

    git clone https://github.com/your-username/Builder-Assistant-Chatbot.git
    cd Builder-Assistant-Chatbot

### 2️⃣ Create and activate virtual environment

    python -m venv .venv
    .venv\Scripts\activate   # On Windows
    source .venv/bin/activate # On Mac/Linux

### 3️⃣ Install dependencies

    pip install -r requirements.txt

### 4️⃣ Configure environment variables

Create a file named .env in the root folder and add your Gemini API key:

    GEMINI_API_KEY=your_api_key_here

⚠️ Never share or push your .env file to GitHub.

### 5️⃣ Run the chatbot

    python app.py

### Open in your browser:

http://127.0.0.1:5000

---

## 📜 Usage

- Type your query in the input box.
- If the query matches predefined FAQs → instant reply.
- If not → Gemini AI will generate a response.

---
## 📦 Dependencies

- Flask
- python-dotenv
- google-genai

    pip install flask python-dotenv google-genai
    
---
## 🛡️ Security Notes

- Keep your API key in .env (already in .gitignore).
- Never hardcode secrets in your code.
- If you ever accidentally commit an API key, revoke it immediately in Google AI Studio.

---
## 🚀 Future Enhancements

- Multi-language support
- Database integration for storing user queries
- Admin dashboard for analytics
- Voice-based chatbot

---
## 👩‍💻 Author

Developed by-Krupali Wayal

---