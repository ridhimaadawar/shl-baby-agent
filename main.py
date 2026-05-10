from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import re
from datetime import datetime
import uuid

app = FastAPI(title="SHL Assessment Agent", description="AI-powered assessment recommendation engine")

# ============================================
# ENHANCED SHL ASSESSMENT CATALOG
# With remote testing, durations, and confidence scores
# ============================================

CATALOG = [
    # HOSPITALITY & SERVICE
    {
        "id": "SHL001",
        "name": "Server - One Sitting (Hospitality Suite)",
        "url": "https://www.shl.com/en/assessments/server-one-sitting/",
        "test_type": "P",
        "keywords": ["server", "waiter", "waitress", "hospitality", "restaurant", "food", "customer service", "entry level", "service", "dining"],
        "duration": 40,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French"],
        "difficulty": "entry",
        "confidence": 0.95
    },
    
    # TECHNICAL - PROGRAMMING
    {
        "id": "SHL002",
        "name": "Java 8 Programming",
        "url": "https://www.shl.com/en/assessments/java-8/",
        "test_type": "K",
        "keywords": ["java", "programming", "developer", "coding", "spring", "backend", "software engineer", "j2ee", "microservices"],
        "duration": 60,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "mid",
        "confidence": 0.98
    },
    {
        "id": "SHL003",
        "name": "Python Programming",
        "url": "https://www.shl.com/en/assessments/python/",
        "test_type": "K",
        "keywords": ["python", "programming", "developer", "coding", "data science", "machine learning", "backend", "django", "flask"],
        "duration": 60,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "mid",
        "confidence": 0.98
    },
    {
        "id": "SHL004",
        "name": "JavaScript Programming",
        "url": "https://www.shl.com/en/assessments/javascript/",
        "test_type": "K",
        "keywords": ["javascript", "js", "frontend", "react", "angular", "vue", "node", "web developer", "typescript"],
        "duration": 60,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "mid",
        "confidence": 0.97
    },
    {
        "id": "SHL005",
        "name": "SQL Programming",
        "url": "https://www.shl.com/en/assessments/sql/",
        "test_type": "K",
        "keywords": ["sql", "database", "data", "query", "mysql", "postgres", "oracle", "dba", "analytics"],
        "duration": 45,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "mid",
        "confidence": 0.96
    },
    {
        "id": "SHL006",
        "name": "C++ Programming",
        "url": "https://www.shl.com/en/assessments/cpp/",
        "test_type": "K",
        "keywords": ["c++", "cpp", "programming", "developer", "coding", "systems", "embedded", "performance"],
        "duration": 60,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "senior",
        "confidence": 0.95
    },
    {
        "id": "SHL007",
        "name": "C# Programming",
        "url": "https://www.shl.com/en/assessments/csharp/",
        "test_type": "K",
        "keywords": ["c#", "csharp", "dotnet", "programming", "developer", "microsoft", ".net", "unity"],
        "duration": 60,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "mid",
        "confidence": 0.95
    },
    
    # PERSONALITY & BEHAVIORAL
    {
        "id": "SHL008",
        "name": "OPQ32r Personality Assessment",
        "url": "https://www.shl.com/en/assessments/opq32r/",
        "test_type": "P",
        "keywords": ["personality", "leadership", "teamwork", "management", "communication", "soft skills", "behavioral", "culture fit", "emotional intelligence"],
        "duration": 25,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French", "German", "Chinese"],
        "difficulty": "all",
        "confidence": 0.99
    },
    {
        "id": "SHL009",
        "name": "Motivation Questionnaire",
        "url": "https://www.shl.com/en/assessments/motivation/",
        "test_type": "P",
        "keywords": ["motivation", "drive", "ambition", "career", "goals", "engagement", "incentive", "passion"],
        "duration": 20,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French"],
        "difficulty": "all",
        "confidence": 0.94
    },
    {
        "id": "SHL010",
        "name": "Work Styles Assessment",
        "url": "https://www.shl.com/en/assessments/work-styles/",
        "test_type": "P",
        "keywords": ["work style", "behavior", "team", "collaboration", "independent", "work habits", "productivity"],
        "duration": 30,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "all",
        "confidence": 0.93
    },
    
    # COGNITIVE & APTITUDE
    {
        "id": "SHL011",
        "name": "Verify G+ Cognitive Ability",
        "url": "https://www.shl.com/en/assessments/verify-g-plus/",
        "test_type": "K",
        "keywords": ["cognitive", "aptitude", "reasoning", "problem solving", "intelligence", "logical", "general ability", "iq"],
        "duration": 36,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French", "German", "Italian", "Dutch"],
        "difficulty": "all",
        "confidence": 0.98
    },
    {
        "id": "SHL012",
        "name": "Numerical Reasoning",
        "url": "https://www.shl.com/en/assessments/numerical-reasoning/",
        "test_type": "K",
        "keywords": ["numerical", "math", "numbers", "data analysis", "quantitative", "statistics", "analytics", "finance"],
        "duration": 18,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French", "German"],
        "difficulty": "all",
        "confidence": 0.97
    },
    {
        "id": "SHL013",
        "name": "Verbal Reasoning",
        "url": "https://www.shl.com/en/assessments/verbal-reasoning/",
        "test_type": "K",
        "keywords": ["verbal", "english", "reading", "comprehension", "writing", "communication", "language", "vocabulary"],
        "duration": 18,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French", "German"],
        "difficulty": "all",
        "confidence": 0.97
    },
    {
        "id": "SHL014",
        "name": "Abstract Reasoning",
        "url": "https://www.shl.com/en/assessments/abstract-reasoning/",
        "test_type": "K",
        "keywords": ["abstract", "logical", "patterns", "visual", "spatial", "deductive", "diagrammatic"],
        "duration": 18,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "all",
        "confidence": 0.96
    },
    {
        "id": "SHL015",
        "name": "Inductive Reasoning",
        "url": "https://www.shl.com/en/assessments/inductive-reasoning/",
        "test_type": "K",
        "keywords": ["inductive", "logical", "patterns", "problem solving", "analytical", "deductive"],
        "duration": 18,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "all",
        "confidence": 0.96
    },
    
    # BUSINESS & MANAGEMENT
    {
        "id": "SHL016",
        "name": "Leadership Assessment",
        "url": "https://www.shl.com/en/assessments/leadership/",
        "test_type": "P",
        "keywords": ["leader", "manager", "leadership", "executive", "director", "supervisor", "team lead", "management"],
        "duration": 40,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French"],
        "difficulty": "senior",
        "confidence": 0.95
    },
    {
        "id": "SHL017",
        "name": "Sales Aptitude Assessment",
        "url": "https://www.shl.com/en/assessments/sales/",
        "test_type": "K",
        "keywords": ["sales", "selling", "business development", "account executive", "b2b", "b2c", "negotiation"],
        "duration": 35,
        "remote_supported": True,
        "languages": ["English", "Spanish"],
        "difficulty": "mid",
        "confidence": 0.94
    },
    {
        "id": "SHL018",
        "name": "Customer Service Assessment",
        "url": "https://www.shl.com/en/assessments/customer-service/",
        "test_type": "P",
        "keywords": ["customer service", "support", "client", "call center", "csr", "client relations", "help desk"],
        "duration": 30,
        "remote_supported": True,
        "languages": ["English", "Spanish", "French"],
        "difficulty": "entry",
        "confidence": 0.95
    },
    {
        "id": "SHL019",
        "name": "Project Management",
        "url": "https://www.shl.com/en/assessments/project-management/",
        "test_type": "K",
        "keywords": ["project manager", "pm", "agile", "scrum", "planning", "coordination", "pmp", "waterfall"],
        "duration": 55,
        "remote_supported": True,
        "languages": ["English"],
        "difficulty": "senior",
        "confidence": 0.94
    },
    
    # ADD YOUR CUSTOM ASSESSMENTS HERE
]

# ============================================
# ADVANCED REQUEST/RESPONSE MODELS
# ============================================

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Dict[str, Any]]] = []
    session_id: Optional[str] = None

class Recommendation(BaseModel):
    name: str
    url: str
    test_type: str
    confidence: Optional[float] = None
    duration: Optional[int] = None

class ChatResponse(BaseModel):
    reply: str
    recommendations: List[Dict[str, Any]]
    end_of_conversation: bool
    session_id: Optional[str] = None
    context_used: Optional[List[str]] = None

# ============================================
# HELPER FUNCTIONS
# ============================================

def extract_duration(text: str) -> Optional[int]:
    """Extract duration constraints from user message"""
    patterns = [
        r'under\s+(\d+)\s*(?:min|minute)',
        r'less than\s+(\d+)\s*(?:min|minute)',
        r'max\s*(\d+)\s*(?:min|minute)',
        r'(\d+)\s*(?:min|minute)s?\s*(?:or less|max)',
        r'(\d+)\s*hour',  # Hours
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            mins = int(match.group(1))
            if 'hour' in pattern:
                mins = mins * 60
            return mins
    return None

def extract_seniority(text: str) -> Optional[str]:
    """Extract seniority level"""
    if any(w in text for w in ['senior', 'lead', 'principal', 'architect']):
        return 'senior'
    if any(w in text for w in ['mid', 'mid-level', 'intermediate', 'experienced']):
        return 'mid'
    if any(w in text for w in ['entry', 'junior', 'fresher', 'graduate']):
        return 'entry'
    return None

def extract_remote_preference(text: str) -> Optional[bool]:
    """Check if remote testing is needed"""
    if any(w in text for w in ['remote', 'online', 'virtual', 'work from home', 'wfh']):
        return True
    if any(w in text for w in ['in-person', 'onsite', 'office']):
        return False
    return None

def calculate_match_score(test: Dict, user_text: str, seniority: Optional[str]) -> float:
    """Calculate sophisticated match score"""
    score = 0.0
    user_text_lower = user_text.lower()
    
    # Keyword matches (primary signal)
    for keyword in test["keywords"]:
        if keyword in user_text_lower:
            score += 1.0
            break  # Only count once per test
    
    # Boost for exact title matches
    job_titles = ["developer", "engineer", "manager", "lead", "server", "waiter"]
    for title in job_titles:
        if title in user_text_lower and title in test["keywords"]:
            score += 0.5
    
    # Seniority alignment
    if seniority and test.get("difficulty") == seniority:
        score += 0.5
    elif seniority == "entry" and test.get("difficulty") == "entry":
        score += 0.3
    
    # Duration preference (penalize long tests if user wants short)
    duration_match = extract_duration(user_text)
    if duration_match and test.get("duration", 999) <= duration_match:
        score += 0.3
    
    # Remote preference
    remote_pref = extract_remote_preference(user_text)
    if remote_pref is True and test.get("remote_supported", False):
        score += 0.2
    
    return score

# ============================================
# HEALTH CHECK
# ============================================

@app.get("/health")
def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# ============================================
# MAIN CHAT ENDPOINT - THE BEAST
# ============================================

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        msg = req.message.lower()
        session_id = req.session_id or str(uuid.uuid4())[:8]
        
        # Get conversation history
        history = req.conversation_history or []
        
        # Build full context
        full_context = msg
        for h in history[-5:]:  # Last 5 messages for context
            if h.get("role") == "user":
                full_context += " " + h.get("content", "").lower()
        
        # Extract constraints
        duration_constraint = extract_duration(full_context)
        seniority = extract_seniority(full_context)
        remote_pref = extract_remote_preference(full_context)
        
        # Calculate scores for all assessments
        scored_matches = []
        for test in CATALOG:
            score = calculate_match_score(test, full_context, seniority)
            if score > 0:
                scored_matches.append({
                    "name": test["name"],
                    "url": test["url"],
                    "test_type": test["test_type"],
                    "score": score,
                    "duration": test.get("duration"),
                    "confidence": test.get("confidence", 0.9),
                    "remote_supported": test.get("remote_supported", False)
                })
        
        # Sort by score (highest first)
        scored_matches.sort(key=lambda x: x["score"], reverse=True)
        
        # Apply filters
        if duration_constraint:
            scored_matches = [m for m in scored_matches if m.get("duration", 999) <= duration_constraint]
        
        if remote_pref is True:
            scored_matches = [m for m in scored_matches if m.get("remote_supported", False)]
        
        # Take top 5
        top_matches = scored_matches[:5]
        
        # === INTELLIGENT RESPONSE GENERATION ===
        
        # Off-topic detection
        off_topic_keywords = ["weather", "news", "sports", "movie", "song", "food recipe", "politics"]
        if any(topic in msg for topic in off_topic_keywords):
            return ChatResponse(
                reply="I'm specifically designed to help with SHL assessment recommendations for hiring. Please tell me about the job role you're recruiting for! 🎯",
                recommendations=[],
                end_of_conversation=False,
                session_id=session_id,
                context_used=["off_topic_filter"]
            )
        
        # Greeting
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        if any(g in msg for g in greetings) and not top_matches:
            return ChatResponse(
                reply="""👋 Hello! I'm your SHL Assessment Agent. I help recruiters find the perfect assessments.

Here's what I can do:
• Recommend technical tests (Java, Python, SQL, etc.)
• Suggest personality & behavioral assessments  
• Filter by duration (e.g., "under 30 minutes")
• Support remote testing preferences
• Match seniority levels (entry/mid/senior)

Try saying: "I need a Java developer under 60 minutes" or "Hiring a remote team leader" 🚀""",
                recommendations=[],
                end_of_conversation=False,
                session_id=session_id,
                context_used=["greeting"]
            )
        
        # Help
        if "help" in msg or "what can you do" in msg or "capabilities" in msg:
            return ChatResponse(
                reply="""📚 **My Capabilities:**

1️⃣ **Technical Assessments** - Java, Python, JavaScript, SQL, C++, C#
2️⃣ **Personality Tests** - OPQ32r, Motivation, Work Styles
3️⃣ **Cognitive Tests** - Numerical, Verbal, Abstract Reasoning
4️⃣ **Business Skills** - Leadership, Sales, Customer Service, Project Management

**Filtering Options:**
• Duration: "under 30 minutes" or "max 60 min"
• Remote: "remote testing" or "online assessment"
• Seniority: "entry level", "mid-level", or "senior"

**Example queries:**
• "I need a senior Java developer under 60 minutes"
• "Looking for a remote project manager"
• "Hiring entry level servers for my restaurant"

What would you like help with? 💪""",
                recommendations=[],
                end_of_conversation=False,
                session_id=session_id,
                context_used=["help"]
            )
        
        # Compare assessments
        if "compare" in msg or "difference between" in msg:
            return ChatResponse(
                reply="""🔍 **Assessment Comparison Guide:**

**Technical (K-type):** Measure hard skills, coding ability, technical knowledge
**Personality (P-type):** Measure soft skills, culture fit, work style, motivation

**Popular combinations:**
• Java Developer → Java Test (K) + OPQ32r (P)
• Manager → Leadership (P) + Numerical Reasoning (K)
• Server → Server Test (P) + Customer Service (P)

Would you like me to recommend a specific combination for your role?""",
                recommendations=[],
                end_of_conversation=False,
                session_id=session_id,
                context_used=["comparison"]
            )
        
        # No matches found
        if not top_matches:
            # Check if we have partial info
            if not any(kw in full_context for kw in ["developer", "engineer", "manager", "server", "lead"]):
                return ChatResponse(
                    reply="I need more information to help you. What job title are you hiring for? (e.g., Java Developer, Project Manager, Server) 🎯",
                    recommendations=[],
                    end_of_conversation=False,
                    session_id=session_id,
                    context_used=["needs_more_info"]
                )
            else:
                return ChatResponse(
                    reply=f"I understand you're hiring for a role related to '{msg[:50]}...' but I couldn't find exact assessment matches. Could you share the top 3 skills required? This will help me find better recommendations. 🔍",
                    recommendations=[],
                    end_of_conversation=False,
                    session_id=session_id,
                    context_used=["no_matches"]
                )
        
        # === SUCCESSFUL RECOMMENDATIONS ===
        
        # Build context message
        context_info = []
        if duration_constraint:
            context_info.append(f"⏱️ Filtered to under {duration_constraint} minutes")
        if seniority:
            context_info.append(f"📊 {seniority.capitalize()} level")
        if remote_pref:
            context_info.append(f"🌐 Remote testing supported")
        
        context_text = "\n".join(context_info) if context_info else ""
        
        # Build recommendations list
        recommendations = []
        for match in top_matches:
            recommendations.append({
                "name": match["name"],
                "url": match["url"],
                "test_type": match["test_type"]
            })
        
        # Determine if conversation should end
        end_convo = len(top_matches) >= 2 and duration_constraint is not None
        
        # Smart reply based on match count
        if len(top_matches) == 1:
            reply = f"""✅ **Perfect Match Found!**

{context_text}

I recommend: **{top_matches[0]['name']}** (Confidence: {int(top_matches[0]['confidence']*100)}%)

This assessment takes {top_matches[0]['duration']} minutes and is {'available for remote testing' if top_matches[0]['remote_supported'] else 'in-person only'}.

Would you like me to recommend additional complementary assessments? 🎯"""
        else:
            reply = f"""🎯 **Top {len(top_matches)} Assessments for Your Role**

{context_text}

Here are my recommendations ranked by relevance:

{chr(10).join([f"{i+1}. **{m['name']}** - {m['duration']} min - {'K' if m['test_type']=='K' else 'P'} type" for i, m in enumerate(top_matches)])}

💡 **Pro Tip:** For comprehensive hiring, combine a technical (K) assessment with a personality (P) assessment.

Need me to filter further? Just tell me! 🚀"""
        
        return ChatResponse(
            reply=reply,
            recommendations=recommendations,
            end_of_conversation=end_convo,
            session_id=session_id,
            context_used=["successful_match", f"found_{len(top_matches)}_matches"]
        )
    
    except Exception as e:
        # Graceful fallback
        return ChatResponse(
            reply="I encountered a small glitch. Could you rephrase your request? Just tell me the job title and skills needed! 🔄",
            recommendations=[],
            end_of_conversation=False,
            session_id=req.session_id or "error",
            context_used=["error_fallback"]
        )

# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
def root():
    return {
        "name": "SHL Assessment Agent - AI-Powered Recommendation Engine",
        "version": "2.0.0",
        "status": "operational",
        "endpoints": {
            "health": "/health - GET",
            "chat": "/chat - POST (main endpoint)",
            "docs": "/docs - Interactive API documentation",
            "redoc": "/redoc - Alternative API docs"
        },
        "features": [
            "Smart keyword matching with scoring",
            "Duration filtering (e.g., 'under 60 minutes')",
            "Seniority level detection (entry/mid/senior)",
            "Remote testing support filtering",
            "Conversation context preservation",
            "Off-topic detection and refusal",
            "Help and comparison commands",
            "Confidence scoring",
            "Multi-language assessment support"
        ],
        "example_queries": [
            "I need a Java developer under 60 minutes",
            "Looking for a remote project manager",
            "Hiring entry level servers",
            "Need leadership assessment for senior manager",
            "Compare technical vs personality tests"
        ]
    }