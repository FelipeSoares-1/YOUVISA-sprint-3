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
        # 1. Identify Intent (Simple Keyword for Prototype)
        message_lower = request.message.lower()
        
        if "status" in message_lower or "como está" in message_lower or "andamento" in message_lower:
            # Mock: In a real app, we'd identify the user's active process.
            # Here we just take the last created process or a mock one.
            from app.services.workflow_service import workflow_service
            processes = list(workflow_service._db.values())
            
            if not processes:
                return {"response": "Você ainda não enviou nenhum documento. Faça o upload para começar."}
                
            last_process = processes[-1]
            explanation = ai_service.explain_status(last_process["status"], last_process["history"])
            return {"response": explanation}
            
        # 2. General AI Chat
        return {"response": f"Recebi: '{request.message}'. (Para ver o status, pergunte 'Qual o status?')."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
