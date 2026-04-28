from __future__ import annotations
import json
from datetime import datetime, timezone
from .connection import get_connection


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create(doc_id: str, filename: str) -> dict:
    now = _now()
    initial_history = json.dumps([{
        "timestamp": now,
        "from_status": None,
        "to_status": "RECEBIDO",
        "description": "Processo criado"
    }])
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO processes (doc_id, filename, status, created_at, updated_at, history)
               VALUES (?, ?, 'RECEBIDO', ?, ?, ?)""",
            (doc_id, filename, now, now, initial_history)
        )
    return get(doc_id)


def get(doc_id: str) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM processes WHERE doc_id = ?", (doc_id,)
        ).fetchone()
    if not row:
        return None
    return _row_to_dict(row)


def list_all() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM processes ORDER BY created_at DESC").fetchall()
    return [_row_to_dict(r) for r in rows]


def update_status(doc_id: str, new_status: str, from_status: str, description: str) -> dict:
    now = _now()
    process = get(doc_id)
    history = process["history"]
    history.append({
        "timestamp": now,
        "from_status": from_status,
        "to_status": new_status,
        "description": description
    })
    with get_connection() as conn:
        conn.execute(
            "UPDATE processes SET status = ?, updated_at = ?, history = ? WHERE doc_id = ?",
            (new_status, now, json.dumps(history), doc_id)
        )
    return get(doc_id)


def update_cv_result(doc_id: str, cv_result: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE processes SET cv_result = ? WHERE doc_id = ?",
            (json.dumps(cv_result), doc_id)
        )


def update_ai_result(doc_id: str, ai_result: dict) -> None:
    with get_connection() as conn:
        conn.execute(
            "UPDATE processes SET ai_result = ? WHERE doc_id = ?",
            (json.dumps(ai_result), doc_id)
        )


def get_latest() -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM processes ORDER BY created_at DESC LIMIT 1"
        ).fetchone()
    return _row_to_dict(row) if row else None


def _row_to_dict(row) -> dict:
    d = dict(row)
    d["history"] = json.loads(d["history"]) if d["history"] else []
    d["cv_result"] = json.loads(d["cv_result"]) if d["cv_result"] else None
    d["ai_result"] = json.loads(d["ai_result"]) if d["ai_result"] else None
    return d
