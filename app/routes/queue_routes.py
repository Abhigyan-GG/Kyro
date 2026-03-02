"""
Kyro — Queue API Routes

GET  /api/queue  — Get the prioritised triage queue
"""

from __future__ import annotations

from flask import Blueprint

from app.core.logging import get_logger
from app.services.queue_service import get_queue
from app.utils.helpers import build_response

logger = get_logger("routes.queue")

queue_bp = Blueprint("queue", __name__, url_prefix="/api/queue")


@queue_bp.route("", methods=["GET"])
def fetch_queue():
    """Return the current triage queue, ordered by severity."""
    queue = get_queue()
    return build_response(data=queue)
