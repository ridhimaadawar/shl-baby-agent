from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# SIMPLE CATALOG - all keys match!
CATALOG = [
    {"name": "Java Test", "url": "https://shl.com/java", "test_type": "K"},
    {"name": "Python Test", "url": "https://shl.com/python", "test_type": "K"},
    {"name": "Server Test", "url": "https://shl.com/server", "test_type": "P"}
]

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[list] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    msg = req.message.lower()
    
    matches = []
    if "java" in msg:
        matches.append(CATALOG[0])
    if "python" in msg:
        matches.append(CATALOG[1])
    if "server" in msg or "waiter" in msg:
        matches.append(CATALOG[2])
    
    if matches:
        # Convert to proper format
        recommendations = []
        for test in matches:
            recommendations.append({
                "name": test["name"],
                "url": test["url"],
                "test_type": test["test_type"]  # ← FIXED!
            })
        
        return {
            "reply": f"Found {len(matches)} tests for you!",
            "recommendations": recommendations,
            "end_of_conversation": True
        }
    
    return {
        "reply": "Tell me: Java, Python, or Server?",
        "recommendations": [],
        "end_of_conversation": False
    }