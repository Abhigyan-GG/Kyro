"""
Kyro — Shared Utility Helpers
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Any, Dict


def utc_now() -> datetime:
    """Current UTC timestamp."""
    return datetime.now(timezone.utc)


def new_uuid() -> str:
    """Generate a new UUID4 string."""
    return str(uuid.uuid4())


def safe_json(obj: Any) -> Any:
    """Make an object JSON-safe (handles UUIDs, datetimes, etc.)."""
    if isinstance(obj, uuid.UUID):
        return str(obj)
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, dict):
        return {k: safe_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [safe_json(i) for i in obj]
    return obj


def build_response(
    data: Any = None,
    message: str = "success",
    status: int = 200,
) -> tuple[Dict[str, Any], int]:
    """Standard API response envelope."""
    body: Dict[str, Any] = {"status": message}
    if data is not None:
        body["data"] = safe_json(data)
    return body, status
