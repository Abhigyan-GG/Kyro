"""
Kyro — Doctor Service

CRUD operations and availability management for doctors.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from app.db.supabase_manager import insert_row, select_by_id, select_rows, update_row
from app.core.errors import NotFoundError, AssignmentError
from app.core.logging import get_logger

logger = get_logger("services.doctor")

TABLE = "doctors"


def create_doctor(data: Dict[str, Any]) -> Dict[str, Any]:
    """Register a new doctor."""
    payload = {
        "name": data["name"],
        "specialization": data["specialization"],
        "max_capacity": data.get("max_capacity", 10),
        "current_load": 0,
        "is_available": data.get("is_available", True),
    }
    doctor = insert_row(TABLE, payload)
    logger.info("Doctor created: id=%s name=%s spec=%s",
                doctor["id"], doctor["name"], doctor["specialization"])
    return doctor


def get_doctor(doctor_id: str) -> Dict[str, Any]:
    """Fetch a single doctor or raise NotFoundError."""
    doctor = select_by_id(TABLE, doctor_id)
    if doctor is None:
        raise NotFoundError(f"Doctor not found: {doctor_id}")
    return doctor


def list_doctors(available_only: bool = False) -> List[Dict[str, Any]]:
    """Return all doctors, optionally filtering to available only."""
    filters = {"is_available": True} if available_only else None
    return select_rows(TABLE, filters=filters, order_by="current_load")


def increment_load(doctor_id: str) -> Dict[str, Any]:
    """
    Increment a doctor's current_load by 1.
    If load reaches max_capacity, mark unavailable.
    """
    doctor = get_doctor(doctor_id)
    new_load = doctor["current_load"] + 1
    updates: Dict[str, Any] = {"current_load": new_load}
    if new_load >= doctor["max_capacity"]:
        updates["is_available"] = False
        logger.warning("Doctor %s reached max capacity (%d)", doctor_id, doctor["max_capacity"])
    return update_row(TABLE, doctor_id, updates)


def get_available_specialist(specialization: str | None = None) -> Optional[Dict[str, Any]]:
    """
    Return the available doctor with the lowest load.
    If specialization is provided, filter by it.
    """
    doctors = list_doctors(available_only=True)
    if specialization:
        doctors = [d for d in doctors if d["specialization"].lower() == specialization.lower()]
    if not doctors:
        return None
    # already sorted by current_load ascending
    return doctors[0]
