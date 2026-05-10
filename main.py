from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

CATALOG = [
    {
        "name": "Server - One Sitting",
        "url": "https://www.shl.com/en/assessments/server-one-sitting/",
        "test_type": "P",
        "skills": ["server", "waiter", "waitress", "hospitality", "customer service", "food", "restaurant"],
        "duration_minutes": 40,
        "remote_testing": True
    },
    {
        "name": "Java 8 Programming",
        "url": "https://www.shl.com/en/assessments/java-8/",
        "test_type": "K",
        "skills": ["java", "programming", "developer", "coding", "spring"],
        "duration_minutes": 60,
        "remote_testing": True
    },
    {
        "name": "OPQ32r - Personality Assessment",
        "url": "https://www.shl.com/en/assessments/opq32r/",
        "test_type": "P",
        "skills": ["personality", "leadership", "teamwork", "communication", "management"],
        "duration_minutes": 25,
        "remote_testing": True
    },
    {
        "name": "Verify G+ - Cognitive Ability",
        "url": "https://www.shl.com/en/assessments/verify-g-plus/",
        "test_type": "K",
        "skills": ["cognitive", "aptitude", "problem solving", "reasoning"],
        "duration_minutes": 36,
        "remote_testing": True
    },
    {
        "name": "Python Programming",
        "url": "https://www.shl.com/en/assessments/python/",
        "test_type": "K",
        "skills": ["python", "programming", "coding", "developer", "data science"],
        "duration_minutes": 60,
        "remote_testing": True
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