from __future__ import annotations
import os
import re
import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from app.agents import OrchestratorAgent
from app.database import interaction_repo

load_dotenv()

logger = logging.getLogger("youvisa.chat")
router = APIRouter()

# ---------------------------------------------------------------------------
# Prompt Injection Protection — input-side filtering
# Blocks attempts to override the system persona or extract instructions.
# ---------------------------------------------------------------------------
_MAX_INPUT_LENGTH = 2000

_INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|my|the)\s+instructions?",
    r"forget\s+(everything|all|your|the)",
    r"esqueça\s+(tudo|as instruções|seu papel)",
    r"ignore\s+(as instruções|tudo)",
    r"\bact\s+as\b",
    r"\bpretend\s+(you\s+are|to\s+be)\b",
    r"\bjailbreak\b",
    r"\bDAN\b",
    r"você\s+(agora\s+)?(é|será)\s+(um|uma)",
    r"new\s+(persona|personality|role|instruction)",
    r"system\s*:\s*",
    r"<\s*system\s*>",
    r"\bprompt\s+injection\b",
]

_INJECTION_RE = re.compile(
    "|".join(_INJECTION_PATTERNS), re.IGNORECASE | re.UNICODE
)

INJECTION_RESPONSE = (
    "Não consigo processar essa mensagem. "
    "Estou aqui para ajudar com dúvidas sobre vistos, passaportes e processos consulares. "
    "Como posso te ajudar?"
)


def _sanitize_input(text: str) -> str | None:
    """Returns sanitized text or None if injection detected."""
    if len(text) > _MAX_INPUT_LENGTH:
        text = text[:_MAX_INPUT_LENGTH]
    if _INJECTION_RE.search(text):
        logger.warning("Prompt injection attempt blocked: %.80s", text)
        return None
    return text


# In-memory session store for chat history (per user_id).
# Interaction logs are persisted in SQLite via the orchestrator.
_session_store: dict[str, list[dict]] = {}
_MAX_HISTORY = 20

# Single orchestrator instance — initialised with Gemini if key is available.
def _build_orchestrator() -> OrchestratorAgent:
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            logger.info("OrchestratorAgent initialised with Gemini")
            return OrchestratorAgent(gemini_client=client)
        except Exception as exc:
            logger.warning("Gemini init failed, falling back to mock: %s", exc)
    return OrchestratorAgent(gemini_client=None)


_orchestrator = _build_orchestrator()


class ChatRequest(BaseModel):
    message: str
    user_id: str = "guest"


@router.post("/")
async def chat_interaction(request: ChatRequest):
    try:
        clean_message = _sanitize_input(request.message)
        if clean_message is None:
            return {
                "response":           INJECTION_RESPONSE,
                "detected_intent":    "GENERAL",
                "intent_confidence":  1.0,
                "entities":           {},
                "has_active_process": False,
            }

        history = _session_store.setdefault(request.user_id, [])

        result = _orchestrator.process(
            user_message=clean_message,
            session_id=request.user_id,
            chat_history=[{"role": m["role"], "content": m["message"]} for m in history],
        )

        history.append({"role": "user",    "message": clean_message})
        history.append({"role": "bot",     "message": result.response})
        if len(history) > _MAX_HISTORY:
            _session_store[request.user_id] = history[-_MAX_HISTORY:]

        return {
            "response":           result.response,
            "detected_intent":    result.intent,
            "intent_confidence":  result.intent_confidence,
            "entities":           result.entities,
            "has_active_process": result.doc_id is not None,
        }
    except Exception as exc:
        logger.exception("Chat error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/history/{user_id}")
async def get_chat_history(user_id: str):
    """Returns the in-session chat history for a given user."""
    return _session_store.get(user_id, [])


@router.get("/interactions/{user_id}")
async def get_interaction_logs(user_id: str):
    """Returns persisted interaction logs (with intent + entities) from SQLite."""
    return interaction_repo.list_by_session(user_id)
