from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# THIS IS THE SHL CATALOG - ADD REAL TESTS HERE!
CATALOG = [
    {
        "name": "Java 8 Programming Test",
        "url": "https://www.shl.com/java8",
        "test_type": "K",
        "skills": ["java", "programming", "developer"]
    },
    {
        "name": "Python Programming Test", 
        "url": "https://www.shl.com/python",
        "test_type": "K",
        "skills": ["python", "programming", "developer"]
    },
    {
        "name": "Leadership Assessment",
        "url": "https://www.shl.com/leadership",
        "test_type": "P",
        "skills": ["leader", "manager", "team lead"]
    },
    {
        "name": "Communication Skills Test",
        "url": "https://www.shl.com/communication",
        "test_type": "P",
        "skills": ["communication", "english", "writing"]
    }
]

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = []

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/chat")
def chat(req: ChatRequest):
    user_message = req.message.lower()
    
    # Find matching tests
    matches = []
    for test in CATALOG:
        for skill in test["skills"]:
            if skill in user_message:
                matches.append({
                    "name": test["name"],
                    "url": test["url"],
                    "test_type": test["type"]
                })
                break
    
    # If we found matches, recommend them
    if matches:
        return {
            "reply": f"I found {len(matches)} tests for you!",
            "recommendations": matches[:5],
            "end_of_conversation": True
        }
    
    # If user said hello
    if "hello" in user_message or "hi" in user_message:
        return {
            "reply": "Hello! Tell me what job you're hiring for (Java developer, manager, etc.)",
            "recommendations": [],
            "end_of_conversation": False
        }
    
    # Otherwise ask for skills
    return {
        "reply": "What skills does the job need? Example: Java, Python, leadership, communication",
        "recommendations": [],
        "end_of_conversation": False
    }