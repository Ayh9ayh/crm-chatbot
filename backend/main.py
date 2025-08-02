from fastapi import Request
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_all_leads
from backend.schemas import LeadQuery
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import chatbot module if available
try:
    from backend.chatbot import process_query
    CHATBOT_AVAILABLE = True
except ImportError:
    CHATBOT_AVAILABLE = False
    print("⚠️ chatbot.py not found. /chat endpoint will not work.")

# Create FastAPI app
app = FastAPI(
    title="CRM Chatbot API",
    description="API for CRM lead management with MongoDB"
)

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health route
@app.get("/")
def root():
    return {"message": "CRM Backend is running!"}

# POST endpoint for chatbot interaction

@app.post("/chat/")
async def chat_endpoint(request: Request):
    if not CHATBOT_AVAILABLE:
        return {"error": "Chatbot functionality not available. Missing chatbot.py."}

    try:
        body = await request.json()
        query = body.get("query", "")
        if not query:
            raise HTTPException(status_code=400, detail="No query provided.")
        
        result = process_query(query)
        # Return the result directly instead of wrapping it in {"message": result}
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# GET endpoint to fetch all leads
@app.get("/leads")
def get_all_leads_endpoint():
    try:
        leads = get_all_leads()
        return {"leads": leads, "count": len(leads)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching leads: {str(e)}")

# Health check route
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "chatbot_available": CHATBOT_AVAILABLE,
        "database": "MongoDB Atlas"
    }
from fastapi import FastAPI, Request
from backend.database import add_new_lead  # we'll create this next

