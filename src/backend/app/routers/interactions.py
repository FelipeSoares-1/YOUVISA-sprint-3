import logging
from fastapi import APIRouter, HTTPException

from app.database import interaction_repo

logger = logging.getLogger("youvisa.interactions")
router = APIRouter()


@router.get("/")
async def list_interactions(limit: int = 100):
    """Returns the most recent interaction logs across all sessions."""
    return interaction_repo.list_all(limit=limit)


@router.get("/session/{session_id}")
async def get_by_session(session_id: str):
    """Returns all interaction logs for a specific user session."""
    logs = interaction_repo.list_by_session(session_id)
    if not logs:
        raise HTTPException(status_code=404, detail="Nenhuma interação encontrada para esta sessão.")
    return logs


@router.get("/doc/{doc_id}")
async def get_by_doc(doc_id: str):
    """Returns all interaction logs related to a specific process/document."""
    return interaction_repo.list_by_doc(doc_id)


@router.get("/stats")
async def interaction_stats():
    """Aggregated stats: total interactions, intent distribution, avg confidence."""
    logs = interaction_repo.list_all(limit=10000)
    if not logs:
        return {"total": 0, "intents": {}, "avg_confidence": 0.0}

    intent_counts: dict[str, int] = {}
    total_conf = 0.0

    for log in logs:
        intent = log.get("detected_intent", "GENERAL")
        intent_counts[intent] = intent_counts.get(intent, 0) + 1
        total_conf += log.get("intent_confidence", 0.0)

    return {
        "total": len(logs),
        "intents": intent_counts,
        "avg_confidence": round(total_conf / len(logs), 3),
    }
