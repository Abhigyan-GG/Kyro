"""
Kyro — Health Check Route

GET /api/health — Simple liveness probe
"""

from flask import Blueprint
from app.utils.helpers import build_response

health_bp = Blueprint("health", __name__, url_prefix="/api")


@health_bp.route("/health", methods=["GET"])
def health_check():
    return build_response(data={"status": "healthy", "service": "kyro-triage-ai"})
