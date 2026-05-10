from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import re

app = FastAPI()

# ============================================
# SHL ASSESSMENT CATALOG
# Add ALL your assessments here!
# ============================================

CATALOG = [
    # HOSPITALITY & SERVICE
    {
        "name": "Server - One Sitting (Hospitality Suite)",
        "url": "https://www.shl.com/en/assessments/server-one-sitting/",
        "test_type": "P",
        "keywords": ["server", "waiter", "waitress", "hospitality", "restaurant", "food", "customer service", "entry level", "service", "dining"],
        "duration": 40
    },
    
    # TECHNICAL - PROGRAMMING
    {
        "name": "Java 8 Programming",
        "url": "https://www.shl.com/en/assessments/java-8/",
        "test_type": "K",
        "keywords": ["java", "programming", "developer", "coding", "spring", "backend", "software engineer", "j2ee"],
        "duration": 60
    },
    {
        "name": "Python Programming",
        "url": "https://www.shl.com/en/assessments/python/",
        "test_type": "K",
        "keywords": ["python", "programming", "developer", "coding", "data science", "machine learning", "backend"],
        "duration": 60
    },
    {
        "name": "JavaScript Programming",
        "url": "https://www.shl.com/en/assessments/javascript/",
        "test_type": "K",
        "keywords": ["javascript", "js", "frontend", "react", "angular", "vue", "node", "web developer"],
        "duration": 60
    },
    {
        "name": "SQL Programming",
        "url": "https://www.shl.com/en/assessments/sql/",
        "test_type": "K",
        "keywords": ["sql", "database", "data", "query", "mysql", "postgres", "oracle", "dba"],
        "duration": 45
    },
    {
        "name": "C++ Programming",
        "url": "https://www.shl.com/en/assessments/cpp/",
        "test_type": "K",
        "keywords": ["c++", "cpp", "programming", "developer", "coding", "systems", "embedded"],
        "duration": 60
    },
    {
        "name": "C# Programming",
        "url": "https://www.shl.com/en/assessments/csharp/",
        "test_type": "K",
        "keywords": ["c#", "csharp", "dotnet", "programming", "developer", "microsoft", ".net"],
        "duration": 60
    },
    
    # PERSONALITY & BEHAVIORAL
    {
        "name": "OPQ32r Personality Assessment",
        "url": "https://www.shl.com/en/assessments/opq32r/",
        "test_type": "P",
        "keywords": ["personality", "leadership", "teamwork", "management", "communication", "soft skills", "behavioral", "culture fit"],
        "duration": 25
    },
    {
        "name": "Motivation Questionnaire",
        "url": "https://www.shl.com/en/assessments/motivation/",
        "test_type": "P",
        "keywords": ["motivation", "drive", "ambition", "career", "goals", "engagement", "incentive"],
        "duration": 20
    },
    {
        "name": "Work Styles Assessment",
        "url": "https://www.shl.com/en/assessments/work-styles/",
        "test_type": "P",
        "keywords": ["work style", "behavior", "team", "collaboration", "independent", "work habits"],
        "duration": 30
    },
    
    # COGNITIVE & APTITUDE
    {
        "name": "Verify G+ Cognitive Ability",
        "url": "https://www.shl.com/en/assessments/verify-g-plus/",
        "test_type": "K",
        "keywords": ["cognitive", "aptitude", "reasoning", "problem solving", "intelligence", "logical", "general ability"],
        "duration": 36
    },
    {
        "name": "Numerical Reasoning",
        "url": "https://www.shl.com/en/assessments/numerical-reasoning/",
        "test_type": "K",
        "keywords": ["numerical", "math", "numbers", "data analysis", "quantitative", "statistics", "analytics"],
        "duration": 18
    },
    {
        "name": "Verbal Reasoning",
        "url": "https://www.shl.com/en/assessments/verbal-reasoning/",
        "test_type": "K",
        "keywords": ["verbal", "english", "reading", "comprehension", "writing", "communication", "language"],
        "duration": 18
    },
    {
        "name": "Abstract Reasoning",
        "url": "https://www.shl.com/en/assessments/abstract-reasoning/",
        "test_type": "K",
        "keywords": ["abstract", "logical", "patterns", "visual", "spatial", "deductive"],
        "duration": 18
    },
    {
        "name": "Inductive Reasoning",
        "url": "https://www.shl.com/en/assessments/inductive-reasoning/",
        "test_type": "K",
        "keywords": ["inductive", "logical", "patterns", "problem solving", "analytical"],
        "duration": 18
    },
    
    # BUSINESS & MANAGEMENT
    {
        "name": "Leadership Assessment",
        "url": "https://www.shl.com/en/assessments/leadership/",
        "test_type": "P",
        "keywords": ["leader", "manager", "leadership", "executive", "director", "supervisor", "team lead"],
        "duration": 40
    },
    {
        "name": "Sales Aptitude Assessment",
        "url": "https://www.shl.com/en/assessments/sales/",
        "test_type": "K",
        "keywords": ["sales", "selling", "business development", "account executive", "b2b", "b2c"],
        "duration": 35
    },
    {
        "name": "Customer Service Assessment",
        "url": "https://www.shl.com/en/assessments/customer-service/",
        "test_type": "P",
        "keywords": ["customer service", "support", "client", "call center", "csr", "client relations"],
        "duration": 30
    },
    {
        "name": "Project Management",
        "url": "https://www.shl.com/en/assessments/project-management/",
        "test_type": "K",
        "keywords": ["project manager", "pm", "agile", "scrum", "planning", "coordination"],
        "duration": 55
    },
    
    # ADD MORE FROM THE SHL CATALOG HERE!
    # Copy-paste from the Excel file you download
]

# ============================================
# REQUEST & RESPONSE MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, Any]]] = []

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Dict[str, Any]]
    end_of_conversation: bool

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
def health():
    return {"status": "ok"}

# ============================================
# MAIN CHAT ENDPOINT
# ============================================

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        msg = req.message.lower()
        
        # Get conversation history for context
        history = req.conversation_history or []
        
        # Combine all messages for better matching
        all_text = msg
        for h in history[-3:]:  # Last 3 messages for context
            if h.get("role") == "user":
                all_text += " " + h.get("content", "").lower()
        
        # Find matching assessments
        matches = []
        for test in CATALOG:
            for keyword in test["keywords"]:
                if keyword in all_text:
                    matches.append({
                        "name": test["name"],
                        "url": test["url"],
                        "test_type": test["test_type"],
                        "score": 1  # Simple scoring
                    })
                    break  # Don't add same test twice per keyword
        
        # Remove duplicates (keep first occurrence)
        seen_names = set()
        unique_matches = []
        for match in matches:
            if match["name"] not in seen_names:
                seen_names.add(match["name"])
                unique_matches.append(match)
        
        # If we found matches, recommend them
        if unique_matches:
            # Limit to top 5 recommendations
            top_matches = unique_matches[:5]
            
            # Build reply message
            if len(top_matches) == 1:
                reply = f"I found 1 assessment for you: {top_matches[0]['name']}"
            else:
                reply = f"I found {len(top_matches)} assessments for you!"
            
            return ChatResponse(
                reply=reply,
                recommendations=[{
                    "name": m["name"],
                    "url": m["url"],
                    "test_type": m["test_type"]
                } for m in top_matches],
                end_of_conversation=True
            )
        
        # Check for greetings
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon"]
        if any(g in msg for g in greetings):
            return ChatResponse(
                reply="Hello! I'm your SHL assessment assistant. Tell me what job you're hiring for (e.g., 'Java developer', 'server', 'project manager') and I'll recommend the right assessments.",
                recommendations=[],
                end_of_conversation=False
            )
        
        # Help message
        if "help" in msg or "what can you do" in msg:
            return ChatResponse(
                reply="I can help you find SHL assessments! Just tell me the job role or skills needed. Examples:\n- 'I need a Java developer'\n- 'Looking for a server'\n- 'Hiring a project manager'\n- 'Need leadership assessment'",
                recommendations=[],
                end_of_conversation=False
            )
        
        # Off-topic
        off_topic = ["weather", "news", "sports", "movie", "song", "food recipe"]
        if any(topic in msg for topic in off_topic):
            return ChatResponse(
                reply="I'm sorry, I can only help with SHL assessment recommendations. Please tell me about the job you're hiring for.",
                recommendations=[],
                end_of_conversation=False
            )
        
        # Default - ask for more info
        return ChatResponse(
            reply="What job role or skills are you hiring for? (e.g., Java developer, server, project manager, Python programmer)",
            recommendations=[],
            end_of_conversation=False
        )
    
    except Exception as e:
        # Fallback response if anything crashes
        return ChatResponse(
            reply="I'm having trouble understanding. Could you tell me the job title or skills you need? (e.g., 'Java developer', 'server', 'manager')",
            recommendations=[],
            end_of_conversation=False
        )

# ============================================
# OPTIONAL: Root endpoint for testing
# ============================================

@app.get("/")
def root():
    return {
        "message": "SHL Assessment Agent is running!",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)",
            "docs": "/docs"
        }
    }