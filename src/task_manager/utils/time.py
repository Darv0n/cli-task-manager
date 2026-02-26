"""Time utilities — ISO 8601 helpers."""

from __future__ import annotations

from datetime import datetime, timezone


def utcnow_iso() -> str:
    """Return current UTC time as ISO 8601 string."""
    return datetime.now(timezone.utc).isoformat()
