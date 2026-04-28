import json
from .connection import get_connection


def save(notification: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO notifications
               (id, doc_id, channel, recipient, sender, subject, body,
                event_type, sent_at, delivered, provider)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                notification["id"],
                notification.get("doc_id", ""),
                notification["channel"],
                notification["recipient"],
                notification["sender"],
                notification.get("subject"),
                notification["body"],
                notification["event_type"],
                notification["sent_at"],
                1 if notification.get("delivered", True) else 0,
                notification["provider"],
            )
        )


def list_all() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM notifications ORDER BY sent_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]


def list_by_doc(doc_id: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM notifications WHERE doc_id = ? ORDER BY sent_at DESC",
            (doc_id,)
        ).fetchall()
    return [dict(r) for r in rows]
