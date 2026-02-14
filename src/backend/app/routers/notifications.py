from fastapi import APIRouter
from app.services.notification_service import notification_service

router = APIRouter()


@router.get("/")
async def list_notifications():
    """Returns all notifications sent by the system (audit trail)."""
    return notification_service.get_all()


@router.get("/{doc_id}")
async def get_notifications_by_doc(doc_id: str):
    """Returns notifications related to a specific document/process."""
    return notification_service.get_by_doc(doc_id)
