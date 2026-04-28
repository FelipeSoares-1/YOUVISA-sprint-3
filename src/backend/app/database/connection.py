import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[3] / "youvisa.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS processes (
                doc_id      TEXT PRIMARY KEY,
                filename    TEXT NOT NULL,
                status      TEXT NOT NULL,
                recipient   TEXT NOT NULL DEFAULT 'cliente@youvisa.com.br',
                created_at  TEXT NOT NULL,
                updated_at  TEXT NOT NULL,
                history     TEXT NOT NULL DEFAULT '[]',
                cv_result   TEXT,
                ai_result   TEXT
            );

            CREATE TABLE IF NOT EXISTS notifications (
                id          TEXT PRIMARY KEY,
                doc_id      TEXT NOT NULL,
                channel     TEXT NOT NULL,
                recipient   TEXT NOT NULL,
                sender      TEXT NOT NULL,
                subject     TEXT,
                body        TEXT NOT NULL,
                event_type  TEXT NOT NULL,
                sent_at     TEXT NOT NULL,
                delivered   INTEGER NOT NULL DEFAULT 1,
                provider    TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS interaction_logs (
                id                  TEXT PRIMARY KEY,
                session_id          TEXT NOT NULL,
                doc_id              TEXT,
                user_message        TEXT NOT NULL,
                detected_intent     TEXT NOT NULL,
                intent_confidence   REAL NOT NULL,
                entities            TEXT NOT NULL DEFAULT '{}',
                agent_trace         TEXT NOT NULL DEFAULT '[]',
                response            TEXT NOT NULL,
                timestamp           TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_interactions_session ON interaction_logs(session_id);
            CREATE INDEX IF NOT EXISTS idx_interactions_doc ON interaction_logs(doc_id);
            CREATE INDEX IF NOT EXISTS idx_notifications_doc ON notifications(doc_id);
        """)
