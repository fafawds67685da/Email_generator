from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Configure API key
genai.configure(api_key="AIzaSyAv1zcbMVtQD2qEB8FUm-_HuQoTogXFWnE")
# Initialize Gemini
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

# FastAPI app
app = FastAPI()

class EmailRequest(BaseModel):
    subject: str
    recipient: str

@app.post("/generate_email/")
async def generate_email(data: EmailRequest):
    prompt = (
        f"Write a professional email to {data.recipient} with the subject '{data.subject}'. "
        "The email should be clear, concise, polite, and end with a formal closing."
    )
    
    try:
        response = model.generate_content(prompt)
        return {"email": response.text}
    except Exception as e:
        return {"error": str(e)}
