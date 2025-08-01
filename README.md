
# AI-Powered Email Generator and Sender

This project is a simple AI-based email assistant that generates and sends professional emails using the Gemini language model and Gmail.

## 🔧 Technologies Used
- **Frontend**: HTML, CSS, JavaScript (Vanilla JS)
- **Backend**: FastAPI (Python)
- **AI Model**: Gemini (via `google.generativeai`)
- **Email Service**: Gmail SMTP

## 📁 Project Structure
```
project/
├── backend/
│   └── main.py               # FastAPI app to generate and send emails
├── frontend/
│   ├── index.html            # UI for input
│   ├── style.css             # Styling
│   └── script.js             # JavaScript to handle frontend logic
└── .env                      # Environment variables (not included)
```

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/email-assistant.git
cd email-assistant
```

### 2. Set Environment Variables
Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_gemini_api_key
EMAIL_ADDRESS=your_email@gmail.com
APP_PASSWORD=your_app_password  # Generate from Gmail -> App Passwords
```

### 3. Install Backend Dependencies
```bash
pip install fastapi uvicorn python-dotenv google-generativeai
```

### 4. Run the Backend
```bash
uvicorn backend.main:app --reload
```

### 5. Open the Frontend
Open `frontend/index.html` in your browser.

## ✅ Features
- Enter a subject and recipient(s)
- Auto-generates a professional email using Gemini
- Sends the email using Gmail SMTP

## 🧠 AI Prompting
If no custom prompt is given, the app defaults to:
> "Write a professional email with the subject '...'. The email should be polite, formal, and clearly communicate the main points... signed as Dev Goyal."

## 🛡️ Disclaimer
Keep your `.env` file private. Don’t expose sensitive data in public repositories.

---
Made with ❤️ by Dev Goyal
