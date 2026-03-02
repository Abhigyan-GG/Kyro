"""
Kyro — Domain Models

Thin data classes representing database entities for in-process use.
Not ORM objects — data is persisted via the Supabase client.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class Patient:
    id: Optional[str] = None
    name: str = ""
    age: int = 0
    gender: str = "other"
    symptoms: List[Dict[str, Any]] = field(default_factory=list)
    vitals: Dict[str, Any] = field(default_factory=dict)
    history: Dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class Doctor:
    id: Optional[str] = None
    name: str = ""
    specialization: str = ""
    max_capacity: int = 10
    current_load: int = 0
    is_available: bool = True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class TriageLog:
    id: Optional[str] = None
    patient_id: str = ""
    severity_level: int = 0
    confidence_score: float = 0.0
    shap_summary: Dict[str, Any] = field(default_factory=dict)
    assigned_doctor_id: Optional[str] = None
    model_version: str = "1.0.0"
    created_at: Optional[datetime] = None
