"""
Kyro — Feature Engineering

Transforms raw patient intake data into a feature vector
suitable for the XGBoost severity model.
"""

from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd

from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("ai.features")

# Symptom category mapping — extend as clinical vocabulary grows
SYMPTOM_CATEGORY_MAP: Dict[str, int] = {
    "respiratory": 0,
    "cardiac": 1,
    "neurological": 2,
    "gastrointestinal": 3,
    "musculoskeletal": 4,
    "dermatological": 5,
    "general": 6,
    "unknown": 7,
}

CHRONIC_CONDITIONS = {
    "diabetes", "hypertension", "asthma", "copd",
    "heart_disease", "cancer", "kidney_disease",
}


def _extract_symptom_category(symptoms: List[Dict[str, Any]]) -> int:
    """Return the highest-priority symptom category code."""
    if not symptoms:
        return SYMPTOM_CATEGORY_MAP["unknown"]
    for s in symptoms:
        cat = s.get("category", "unknown").lower()
        if cat in SYMPTOM_CATEGORY_MAP:
            return SYMPTOM_CATEGORY_MAP[cat]
    return SYMPTOM_CATEGORY_MAP["unknown"]


def _has_chronic_condition(history: Dict[str, Any]) -> int:
    """Binary flag: 1 if patient has any known chronic condition."""
    conditions = history.get("chronic_conditions", [])
    if isinstance(conditions, list):
        for c in conditions:
            if str(c).lower() in CHRONIC_CONDITIONS:
                return 1
    return 0


def build_feature_vector(patient_data: Dict[str, Any]) -> pd.DataFrame:
    """
    Convert a patient intake dict into a single-row DataFrame
    with the columns expected by the model.

    Parameters
    ----------
    patient_data : dict
        Must contain keys: age, vitals (dict), symptoms (list), history (dict).

    Returns
    -------
    pd.DataFrame with one row and all feature columns.
    """
    vitals = patient_data.get("vitals", {})

    features = {
        # Numerical
        "age":                patient_data.get("age", 0),
        "heart_rate":         vitals.get("heart_rate", 0.0),
        "systolic_bp":        vitals.get("systolic_bp", 0.0),
        "diastolic_bp":       vitals.get("diastolic_bp", 0.0),
        "oxygen_saturation":  vitals.get("oxygen_saturation", 0.0),
        "temperature":        vitals.get("temperature", 0.0),
        # Categorical (encoded)
        "symptom_category":   _extract_symptom_category(patient_data.get("symptoms", [])),
        "has_chronic_condition": _has_chronic_condition(patient_data.get("history", {})),
    }

    df = pd.DataFrame([features])
    logger.debug("Feature vector built: %s", features)
    return df


def get_feature_names() -> List[str]:
    """Return ordered feature column names used by the model."""
    return settings.ai.NUMERICAL_FEATURES + settings.ai.CATEGORICAL_FEATURES
