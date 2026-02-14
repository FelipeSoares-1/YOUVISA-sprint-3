from datetime import datetime
from typing import List, Dict
import logging
import json

logger = logging.getLogger("youvisa.notifications")


class NotificationService:
    def __init__(self):
        self._notifications: List[Dict] = []

    def notify(self, recipient: str, event_type: str, message: str, doc_id: str = None):
        """
        Registers and simulates sending a notification.
        All notifications are persisted in-memory for audit trail.
        """
        notification = {
            "id": len(self._notifications) + 1,
            "recipient": recipient,
            "event_type": event_type,
            "message": message,
            "doc_id": doc_id,
            "channel": "email",
            "sent_at": datetime.now().isoformat(),
            "delivered": True
        }

        self._notifications.append(notification)

        # Structured log (JSON)
        log_entry = json.dumps(notification, ensure_ascii=False)
        logger.info(f"[NOTIFICATION] {log_entry}")
        print(f"📧 [NOTIFICAÇÃO] Para: {recipient} | Evento: {event_type} | {message}")

        return notification

    def get_all(self) -> List[Dict]:
        return self._notifications

    def get_by_doc(self, doc_id: str) -> List[Dict]:
        return [n for n in self._notifications if n.get("doc_id") == doc_id]


notification_service = NotificationService()
