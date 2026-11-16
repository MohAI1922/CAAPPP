"""
VeriMath — Teacher Dashboard API Router
========================================
FastAPI router for the /dashboard/* endpoints.
Reads telemetry data from Firebase Firestore and exposes it to
the teacher's browser on the same LAN.
"""

from __future__ import annotations

import logging
import os
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.dashboard.gemini_summary import generate_summary
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/dashboard", tags=["dashboard"])

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "")
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "")

# ─────────────────────────────────────────────────────────────────────────────
# Firebase client (lazy singleton)
# ─────────────────────────────────────────────────────────────────────────────

_db = None


def _get_db():
    global _db
    if _db is not None:
        return _db

    if not SERVICE_ACCOUNT_PATH or not os.path.exists(SERVICE_ACCOUNT_PATH):
        logger.warning("Firebase not configured — dashboard will return empty data.")
        return None

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore

        if not firebase_admin._apps:
            cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
            firebase_admin.initialize_app(cred)

        _db = firestore.client()
        return _db
    except Exception as e:
        logger.error(f"Firebase init failed: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# Response models
# ─────────────────────────────────────────────────────────────────────────────

class StatsResponse(BaseModel):
    total_problems: int
    verified_count: int
    rejected_count: int
    unsupported_count: int
    pass_rate: float            # verified / total (0.0–1.0)
    avg_elapsed_ms: float
    avg_retry_count: float


class RecentEvent(BaseModel):
    problem_id: str
    timestamp: str
    problem_text: str
    template_id: Optional[str]
    lean_verdict: str
    elapsed_ms: int
    from_cache: bool


class SummaryResponse(BaseModel):
    summary: str
    event_count_analyzed: int
    generated_at: str


# ─────────────────────────────────────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────────────────────────────────────

@router.get("/stats", response_model=StatsResponse)
async def get_stats():
    """Aggregated statistics for all problems in this session."""
    events = _fetch_events(limit=500)

    if not events:
        return StatsResponse(
            total_problems=0, verified_count=0, rejected_count=0,
            unsupported_count=0, pass_rate=0.0, avg_elapsed_ms=0.0,
            avg_retry_count=0.0,
        )

    total = len(events)
    verified = sum(1 for e in events if e.get("lean_verdict") == "VERIFIED")
    rejected = sum(1 for e in events if e.get("lean_verdict") in ("REJECTED", "TIMEOUT", "SYNTAX_ERROR"))
    unsupported = sum(1 for e in events if e.get("lean_verdict") == "UNSUPPORTED")

    avg_elapsed = sum(e.get("total_elapsed_ms", 0) for e in events) / total
    avg_retries = sum(e.get("retry_count", 0) for e in events) / total

    return StatsResponse(
        total_problems=total,
        verified_count=verified,
        rejected_count=rejected,
        unsupported_count=unsupported,
        pass_rate=round(verified / total, 3) if total > 0 else 0.0,
        avg_elapsed_ms=round(avg_elapsed, 1),
        avg_retry_count=round(avg_retries, 2),
    )


@router.get("/recent", response_model=list[RecentEvent])
async def get_recent(limit: int = 20):
    """Most recent N problem events."""
    events = _fetch_events(limit=limit)
    return [
        RecentEvent(
            problem_id=e.get("problem_id", ""),
            timestamp=e.get("timestamp", ""),
            problem_text=e.get("problem_text", "")[:100],
            template_id=e.get("template_id"),
            lean_verdict=e.get("lean_verdict", "UNKNOWN"),
            elapsed_ms=e.get("total_elapsed_ms", 0),
            from_cache=e.get("from_cache", False),
        )
        for e in events
    ]


@router.get("/failures", response_model=list[RecentEvent])
async def get_failures():
    """Problems that were rejected or caused errors."""
    events = _fetch_events(limit=200)
    failures = [
        e for e in events
        if e.get("lean_verdict") in ("REJECTED", "TIMEOUT", "SYNTAX_ERROR", "ERROR")
    ]
    return [
        RecentEvent(
            problem_id=e.get("problem_id", ""),
            timestamp=e.get("timestamp", ""),
            problem_text=e.get("problem_text", "")[:100],
            template_id=e.get("template_id"),
            lean_verdict=e.get("lean_verdict", "UNKNOWN"),
            elapsed_ms=e.get("total_elapsed_ms", 0),
            from_cache=e.get("from_cache", False),
        )
        for e in failures
    ]


@router.get("/summary", response_model=SummaryResponse)
async def get_summary():
    """AI-generated summary of the session using Gemini API."""
    from datetime import datetime, timezone
    events = _fetch_events(limit=50)

    if not events:
        return SummaryResponse(
            summary="No problems have been solved yet in this session.",
            event_count_analyzed=0,
            generated_at=datetime.now(timezone.utc).isoformat(),
        )

    summary_text = await generate_summary(events)

    return SummaryResponse(
        summary=summary_text,
        event_count_analyzed=len(events),
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Firestore query helper
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_events(limit: int = 100) -> list[dict[str, Any]]:
    """Fetch events from Firestore if available, otherwise fallback to local SQLite store."""
    db = _get_db()
    if db is not None:
        try:
            docs = (
                db.collection("verimath_events")
                .order_by("timestamp", direction="DESCENDING")
                .limit(limit)
                .stream()
            )
            cloud_events = [doc.to_dict() for doc in docs]
            if cloud_events:
                return cloud_events
        except Exception as e:
            logger.error(f"Firestore query failed: {e}")

    # Offline / local development fallback
    try:
        from backend.iot.event_store import get_events
        return get_events(limit=limit)
    except Exception as e:
        logger.warning(f"Local event store query failed: {e}")
        return []
