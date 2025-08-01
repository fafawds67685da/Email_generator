from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from email.mime.text import MIMEText
import smtplib
import os
import google.generativeai as genai

# === 1. Load Gemini API key securely ===
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_FALLBACK_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# === 2. Define the function to generate email body using Gemini ===
def generate_email_content(prompt: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"LLM Error: {str(e)}"

# === 3. Define FastAPI app ===
app = FastAPI()

# === 4. Request Model ===
class EmailRequest(BaseModel):
    subject: str
    recipient: str
    message: Optional[str] = None  # optional if generating via LLM

# === 5. Endpoint to send email ===
@app.post("/send_email/")
async def send_email(data: EmailRequest):
    # Generate prompt for LLM if message not provided
    if not data.message:
        prompt = (
            f"Write a professional email to {data.recipient} with the subject '{data.subject}'. "
            "The email should be clear, concise, polite, and end with a formal closing."
        )
        data.message = generate_email_content(prompt)

    # Compose the email
    msg = MIMEText(data.message)
    msg["Subject"] = data.subject
    msg["From"] = os.getenv("EMAIL_ADDRESS", "your_email@gmail.com")
    msg["To"] = data.recipient

    # Send the email via Gmail SMTP (You can update this for other providers)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("APP_PASSWORD"))
            smtp.send_message(msg)
        return {
            "status": "✅ Email sent successfully",
            "llm_output": data.message
        }
    except Exception as e:
        return {"error": str(e)}
