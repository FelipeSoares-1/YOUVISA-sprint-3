from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List
from app.services.ai_service import ai_service

router = APIRouter()

# Conversation context storage (session-based)
conversation_store: Dict[str, List[dict]] = {}

class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"


# Intent Classification (keyword + pattern matching)
INTENT_PATTERNS = {
    "STATUS_QUERY": [
        "status", "como está", "andamento", "situação", "onde está",
        "em que pé", "qual o estado", "como vai", "atualização"
    ],
    "MISSING_DOCS": [
        "falta", "faltando", "pendente", "documento faltando",
        "está faltando", "o que falta", "preciso enviar", "incompleto"
    ],
    "NEXT_STEP": [
        "próximo passo", "próxima etapa", "o que fazer", "preciso fazer",
        "o que acontece agora", "qual o próximo", "como proceder", "o que devo"
    ],
    "DEADLINE": [
        "prazo", "quanto tempo", "quando fica pronto", "demora",
        "previsão", "estimativa", "dias", "quando termina"
    ],
    "GREETING": [
        "olá", "oi", "bom dia", "boa tarde", "boa noite", "hello", "hey"
    ],
}


def classify_intent(message: str) -> str:
    message_lower = message.lower()
    scores = {}
    for intent, keywords in INTENT_PATTERNS.items():
        score = sum(1 for kw in keywords if kw in message_lower)
        if score > 0:
            scores[intent] = score
    if not scores:
        return "GENERAL"
    return max(scores, key=scores.get)


def get_latest_process():
    from app.services.workflow_service import workflow_service
    items = list(workflow_service._db.items())
    if not items:
        return None, None
    doc_id, process = items[-1]
    return doc_id, process


@router.post("/")
async def chat_interaction(request: ChatRequest):
    try:
        intent = classify_intent(request.message)

        # Initialize conversation context for this user
        if request.user_id not in conversation_store:
            conversation_store[request.user_id] = []

        # Store user message
        conversation_store[request.user_id].append({
            "role": "user",
            "message": request.message,
            "intent": intent
        })

        doc_id, process = get_latest_process()

        response_text = ""

        if intent == "GREETING":
            response_text = (
                "Olá! 👋 Sou o assistente virtual YOUVISA. "
                "Posso te ajudar com o status do seu processo, "
                "informar sobre documentos pendentes ou explicar os próximos passos. "
                "Como posso ajudar?"
            )

        elif intent == "STATUS_QUERY":
            if not process:
                response_text = "Você ainda não possui nenhum processo ativo. Envie seu documento para começar!"
            else:
                explanation = ai_service.explain_status(
                    process["status"],
                    process.get("history", [])
                )
                response_text = explanation

        elif intent == "MISSING_DOCS":
            if not process:
                response_text = "Nenhum processo encontrado. Envie seu documento primeiro."
            elif process["status"] == "PENDENTE_DOCS":
                response_text = (
                    "⚠️ Sim, identificamos uma pendência na sua documentação. "
                    "Pode ter ocorrido um problema de legibilidade ou falta de uma página. "
                    "Por favor, reenvie o documento atualizado pelo painel."
                )
            elif process["status"] == "RECEBIDO":
                response_text = (
                    "Seu documento foi recebido e aguarda análise. "
                    "Se houver alguma pendência, você será notificado automaticamente."
                )
            else:
                response_text = (
                    f"Seu processo está no status '{process['status']}'. "
                    "No momento, não há pendência de documentos registrada."
                )

        elif intent == "NEXT_STEP":
            if not process:
                response_text = "Envie seu documento para iniciarmos o processo de análise."
            else:
                next_steps = {
                    "RECEBIDO": "Seu documento será encaminhado para análise técnica. Aguarde a validação automática.",
                    "EM_ANALISE": "Nossa equipe está validando seus dados. Após a análise, você receberá uma notificação com o resultado.",
                    "PENDENTE_DOCS": "Reenvie o documento pendente pelo painel. Após o reenvio, ele voltará para análise.",
                    "APROVADO": "Sua documentação foi aprovada! O próximo passo é aguardar a emissão do visto.",
                    "REPROVADO": "Infelizmente seu processo foi reprovado. Entre em contato com o suporte para entender os motivos.",
                }
                response_text = next_steps.get(
                    process["status"],
                    "Não foi possível determinar o próximo passo."
                )

        elif intent == "DEADLINE":
            # Guardrail: NEVER invent deadlines
            response_text = (
                "⏳ Por política de governança, não podemos informar prazos exatos, "
                "pois cada processo depende da complexidade da documentação e do volume de solicitações. "
                "Recomendamos acompanhar o status pelo painel ou chatbot. "
                "Você será notificado automaticamente a cada mudança de etapa."
            )

        else:
            # GENERAL fallback with context awareness
            if process:
                response_text = (
                    f"Entendi sua mensagem. Seu processo atual está no status: "
                    f"**{process['status']}**. "
                    "Posso ajudar com: status detalhado, documentos pendentes, "
                    "próximos passos ou prazos. O que você precisa?"
                )
            else:
                response_text = (
                    "Recebi sua mensagem! Posso ajudar com informações sobre "
                    "status de processos, documentos pendentes e próximos passos. "
                    "Envie seu documento pelo painel para começar."
                )

        # Store bot response in conversation context
        conversation_store[request.user_id].append({
            "role": "bot",
            "message": response_text,
            "intent": intent
        })

        # Keep only last 20 messages per user
        if len(conversation_store[request.user_id]) > 20:
            conversation_store[request.user_id] = conversation_store[request.user_id][-20:]

        return {
            "response": response_text,
            "intent_detected": intent,
            "has_active_process": process is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history/{user_id}")
async def get_chat_history(user_id: str):
    return conversation_store.get(user_id, [])
