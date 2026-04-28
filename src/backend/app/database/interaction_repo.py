import json
from .connection import get_connection


def save(log: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO interaction_logs
               (id, session_id, doc_id, user_message, detected_intent,
                intent_confidence, entities, agent_trace, response, timestamp)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                log["id"],
                log["session_id"],
                log.get("doc_id"),
                log["user_message"],
                log["detected_intent"],
                log["intent_confidence"],
                json.dumps(log.get("entities", {})),
                json.dumps(log.get("agent_trace", [])),
                log["response"],
                log["timestamp"],
            )
        )


def list_all(limit: int = 100) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM interaction_logs ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return [_parse(r) for r in rows]


def list_by_session(session_id: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM interaction_logs WHERE session_id = ? ORDER BY timestamp ASC",
            (session_id,)
        ).fetchall()
    return [_parse(r) for r in rows]


def list_by_doc(doc_id: str) -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM interaction_logs WHERE doc_id = ? ORDER BY timestamp ASC",
            (doc_id,)
        ).fetchall()
    return [_parse(r) for r in rows]


def _parse(row) -> dict:
    d = dict(row)
    d["entities"] = json.loads(d["entities"]) if d["entities"] else {}
    d["agent_trace"] = json.loads(d["agent_trace"]) if d["agent_trace"] else []
    return d
