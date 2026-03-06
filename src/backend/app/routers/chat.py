from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.services.ai_service import ai_service
from app.services.workflow_service import workflow_service

router = APIRouter()

# Conversation context storage (session-based)
conversation_store: Dict[str, List[dict]] = {}

class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"

def get_latest_process():
    items = list(workflow_service._db.items())
    if not items:
        return None, None
    doc_id, process = items[-1]
    return doc_id, process

@router.post("/")
async def chat_interaction(request: ChatRequest):
    try:
        # Initialize conversation context for this user
        if request.user_id not in conversation_store:
            conversation_store[request.user_id] = []

        # Store user message
        conversation_store[request.user_id].append({
            "role": "user",
            "message": request.message
        })

        doc_id, process = get_latest_process()

        # Send to conversational AI
        response_text = ai_service.chat_conversational(
            user_message=request.message,
            chat_history=conversation_store[request.user_id],
            process=process
        )

        # Store bot response in conversation context
        conversation_store[request.user_id].append({
            "role": "bot",
            "message": response_text
        })

        # Keep only last 20 messages per user
        if len(conversation_store[request.user_id]) > 20:
            conversation_store[request.user_id] = conversation_store[request.user_id][-20:]

        return {
            "response": response_text,
            "has_active_process": process is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{user_id}")
async def get_chat_history(user_id: str):
    return conversation_store.get(user_id, [])
