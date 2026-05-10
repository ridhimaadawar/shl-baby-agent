from fastapi import FastAPI
from groq import Groq
import os

app = FastAPI()
client = Groq(api_key="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")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(request: dict):
    user_message = request.get("message", "")
    
    # If user says hello, say hello back
    if "hello" in user_message.lower():
        return {
            "reply": "Hello! I help find SHL tests. What job are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }
    
    # For everything else, ask a question
    return {
        "reply": "What skills does the job need? Like Java, Python, or leadership?",
        "recommendations": [],
        "end_of_conversation": False
    }