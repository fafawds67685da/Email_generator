from typing import List
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
import smtplib
import os
import google.generativeai as genai
from email.mime.text import MIMEText

# === 1. Load Gemini API key securely ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_FALLBACK_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# === 2. Generate email body ===
def generate_email_content(subject: str, prompt: str = "") -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        if not prompt:
            prompt = (
                f"Write a professional email with the subject '{subject}'. "
                "The email should be polite, formal, and clearly communicate the main points related to the subject. "
                "It should include a greeting, a concise message, and a formal closing with my name as Dev Goyal."
            )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LLM Error: {str(e)}"

# === 3. FastAPI app ===
app = FastAPI()

# === 4. Request Model ===
class EmailRequest(BaseModel):
    subject: str
    recipients: List[str]
    prompt: str = ""

# === 5. Send email to multiple recipients ===
@app.post("/send_email/")
async def send_email(data: EmailRequest):
    email_body = generate_email_content(data.subject, data.prompt)

    sender_email = os.getenv("EMAIL_ADDRESS", "your_email@gmail.com")
    app_password = os.getenv("APP_PASSWORD")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(sender_email, app_password)
            for recipient in data.recipients:
                msg = MIMEText(email_body)
                msg["Subject"] = data.subject
                msg["From"] = sender_email
                msg["To"] = recipient
                smtp.send_message(msg)

        return {
            "status": "✅ Email sent to all recipients successfully",
            "email_body": email_body,
            "recipients": data.recipients
        }
    except Exception as e:
        return {"error": str(e)}
