"""
VeriMath — Local Telemetry Event Store
======================================
SQLite-backed persistent local event store for telemetry events.
Ensures the Teacher Dashboard works out-of-the-box in local development,
offline classroom use, and Raspberry Pi deployments even without
external Mosquitto or cloud Firebase credentials.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Any, Optional

logger = logging.getLogger(__name__)

DEFAULT_DB_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "..", "telemetry_events.db")
)
EVENT_DB_PATH = os.getenv("TELEMETRY_DB_PATH", DEFAULT_DB_PATH)


def init_db(db_path: str = EVENT_DB_PATH) -> None:
    """Initialize the telemetry events table if it does not exist."""
    try:
        os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS telemetry_events (
                    problem_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    problem_text TEXT NOT NULL,
                    template_id TEXT,
                    candidate_answer TEXT,
                    lean_statement TEXT,
                    lean_verdict TEXT NOT NULL,
                    judge_verdict TEXT,
                    retry_count INTEGER NOT NULL DEFAULT 0,
                    total_elapsed_ms INTEGER NOT NULL DEFAULT 0,
                    from_cache INTEGER NOT NULL DEFAULT 0,
                    student_id TEXT DEFAULT 'anonymous'
                )
            """)
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_events_timestamp 
                ON telemetry_events(timestamp DESC)
            """)
            conn.commit()
    except Exception as e:
        logger.error(f"Failed to initialize telemetry SQLite database: {e}")


def record_event(event_dict: dict[str, Any], db_path: str = EVENT_DB_PATH) -> None:
    """Insert or replace a telemetry event into local SQLite storage."""
    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO telemetry_events (
                    problem_id, timestamp, problem_text, template_id,
                    candidate_answer, lean_statement, lean_verdict,
                    judge_verdict, retry_count, total_elapsed_ms,
                    from_cache, student_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event_dict.get("problem_id", ""),
                event_dict.get("timestamp") or datetime.now(timezone.utc).isoformat(),
                event_dict.get("problem_text", ""),
                event_dict.get("template_id"),
                event_dict.get("candidate_answer"),
                event_dict.get("lean_statement"),
                event_dict.get("lean_verdict", "UNKNOWN"),
                event_dict.get("judge_verdict"),
                int(event_dict.get("retry_count", 0)),
                int(event_dict.get("total_elapsed_ms", 0)),
                1 if event_dict.get("from_cache") else 0,
                event_dict.get("student_id", "anonymous"),
            ))
            conn.commit()
    except Exception as e:
        logger.warning(f"Failed to record telemetry event to local SQLite: {e}")


def get_events(limit: int = 100, db_path: str = EVENT_DB_PATH) -> list[dict[str, Any]]:
    """Fetch recent telemetry events from local SQLite storage."""
    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM telemetry_events
                ORDER BY timestamp DESC
                LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            return [
                {
                    "problem_id": r["problem_id"],
                    "timestamp": r["timestamp"],
                    "problem_text": r["problem_text"],
                    "template_id": r["template_id"],
                    "candidate_answer": r["candidate_answer"],
                    "lean_statement": r["lean_statement"],
                    "lean_verdict": r["lean_verdict"],
                    "judge_verdict": r["judge_verdict"],
                    "retry_count": r["retry_count"],
                    "total_elapsed_ms": r["total_elapsed_ms"],
                    "from_cache": bool(r["from_cache"]),
                    "student_id": r["student_id"],
                }
                for r in rows
            ]
    except Exception as e:
        logger.warning(f"Failed to query local telemetry events: {e}")
        return []
