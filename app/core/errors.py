"""
Kyro — Structured Error Handling

Custom exception hierarchy for consistent API error responses.
"""

from __future__ import annotations
from typing import Any, Dict, Optional


class KyroError(Exception):
    """Base exception for all Kyro application errors."""

    status_code: int = 500
    error_type: str = "INTERNAL_ERROR"

    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "error": self.error_type,
            "message": self.message,
        }
        if self.details:
            payload["details"] = self.details
        return payload


class ValidationError(KyroError):
    """Raised when request data fails validation."""
    status_code = 400
    error_type = "VALIDATION_ERROR"


class NotFoundError(KyroError):
    """Raised when a requested resource does not exist."""
    status_code = 404
    error_type = "NOT_FOUND"


class DatabaseError(KyroError):
    """Raised when a database operation fails."""
    status_code = 502
    error_type = "DATABASE_ERROR"


class AIModelError(KyroError):
    """Raised when the AI inference pipeline fails."""
    status_code = 500
    error_type = "AI_MODEL_ERROR"


class AssignmentError(KyroError):
    """Raised when doctor assignment logic fails."""
    status_code = 500
    error_type = "ASSIGNMENT_ERROR"
