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

# === 2. Define the function to generate email body using Gemini ===
def generate_email_content(subject: str, recipient: str) -> str:
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        # Generate a prompt specifically requesting both the subject and body
        prompt = (
            f"Write a professional email to {recipient} with the subject '{subject}'. "
            "The email should be polite, formal, and clearly communicate the main points related to the subject. "
            "It should include a greeting, a concise message, and a formal closing. with my name as Dev Goyal nothing else at the end"
        )
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

# === 5. Endpoint to send email ===
@app.post("/send_email/")
async def send_email(data: EmailRequest):
    # Generate the full email content using the subject and recipient
    email_body = generate_email_content(data.subject, data.recipient)

    # Compose the email
    msg = MIMEText(email_body)
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
            "email_body": email_body  # Include the full email content sent to the recipient
        }
    except Exception as e:
        return {"error": str(e)}
