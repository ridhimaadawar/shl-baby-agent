from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

app = FastAPI()

# SHL CATALOG - REAL ASSESSMENTS
CATALOG = [
    {
        "name": "Server - One Sitting",
        "url": "https://www.shl.com/en/assessments/server-one-sitting/",
        "test_type": "P",
        "skills": ["server", "waiter", "waitress", "hospitality", "customer service"]
    },
    {
        "name": "Java 8 Programming",
        "url": "https://www.shl.com/en/assessments/java-8/",
        "test_type": "K",
        "skills": ["java", "programming", "developer"]
    },
    {
        "name": "OPQ32r Personality",
        "url": "https://www.shl.com/en/assessments/opq32r/",
        "test_type": "P",
        "skills": ["leadership", "personality", "teamwork", "management"]
    },
    {
        "name": "Python Programming",
        "url": "https://www.shl.com/en/assessments/python/",
        "test_type": "K",
        "skills": ["python", "programming", "developer"]
    }
]

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, Any]]] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    try:
        user_message = req.message.lower()
        
        # Find matching assessments
        matches = []
        for test in CATALOG:
            for skill in test["skills"]:
                if skill in user_message:
                    matches.append({
                        "name": test["name"],
                        "url": test["url"],
                        "test_type": test["test_type"]
                    })
                    break
        
        # If we found matches
        if matches:
            return {
                "reply": f"Great! I found {len(matches)} assessments for you.",
                "recommendations": matches[:5],
                "end_of_conversation": True
            }
        
        # If user said hello
        if any(word in user_message for word in ["hello", "hi", "hey"]):
            return {
                "reply": "Hello! Tell me what job you're hiring for (like Java developer, server, manager).",
                "recommendations": [],
                "end_of_conversation": False
            }
        
        # Default - ask for more info
        return {
            "reply": "What skills does the job need? Try: 'Java developer', 'Python programmer', 'server', or 'manager'",
            "recommendations": [],
            "end_of_conversation": False
        }
    
    except Exception as e:
        # If anything crashes, return a safe response
        return {
            "reply": "I'm having trouble understanding. Can you tell me the job title or skills needed?",
            "recommendations": [],
            "end_of_conversation": False
        }