from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"

@router.post("/")
async def chat_interaction(request: ChatRequest):
    try:
        # 1. Identify Intent (NLP)
        intent_response = ai_service.analyze_document(request.message) 
        # Using same method for now, but in real app would have specific 'detect_intent'
        
        # 2. Respond
        if "simulado" in str(intent_response).lower():
            return {"response": "Entendi. Parece que você quer enviar um documento. Por favor, faça o upload na área ao lado."}
            
        return {"response": f"Recebi sua mensagem: '{request.message}'. Como posso ajudar com seu visto hoje?"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
