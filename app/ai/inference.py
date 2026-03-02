"""
Kyro — AI Inference Pipeline

Loads the trained XGBoost model and provides:
  • predict_severity()  — severity class + confidence
  • explain_prediction() — SHAP feature importance
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Dict, Tuple

import numpy as np
import pandas as pd
import shap
from xgboost import XGBClassifier

from app.ai.features import build_feature_vector, get_feature_names
from app.core.config import settings
from app.core.errors import AIModelError
from app.core.logging import get_logger

logger = get_logger("ai.inference")

# Module-level cache
_model: XGBClassifier | None = None
_explainer: shap.TreeExplainer | None = None


def _load_model() -> XGBClassifier:
    """Load XGBoost model from disk (cached)."""
    global _model
    if _model is not None:
        return _model

    model_path = settings.ai.MODEL_PATH
    if not Path(model_path).exists():
        raise AIModelError(
            f"Model file not found at '{model_path}'. "
            "Run `python -m app.ai.train` first."
        )

    _model = XGBClassifier()
    _model.load_model(model_path)
    logger.info("XGBoost model loaded from %s", model_path)
    return _model


def _get_explainer() -> shap.TreeExplainer:
    """Return a SHAP TreeExplainer (cached)."""
    global _explainer
    if _explainer is None:
        _explainer = shap.TreeExplainer(_load_model())
        logger.info("SHAP TreeExplainer initialised")
    return _explainer


def predict_severity(patient_data: Dict[str, Any]) -> Tuple[int, float, np.ndarray]:
    """
    Predict severity for a single patient.

    Parameters
    ----------
    patient_data : dict
        Raw patient intake dict (age, vitals, symptoms, history).

    Returns
    -------
    (severity_level, confidence_score, probabilities)
    """
    try:
        model = _load_model()
        X = build_feature_vector(patient_data)
        proba = model.predict_proba(X)[0]  # shape (4,)
        severity = int(np.argmax(proba))
        confidence = float(proba[severity])

        logger.info(
            "Prediction: severity=%d  confidence=%.3f  proba=%s",
            severity, confidence, proba.round(3).tolist(),
        )
        return severity, confidence, proba
    except AIModelError:
        raise
    except Exception as exc:
        logger.exception("Severity prediction failed")
        raise AIModelError(f"Prediction failed: {exc}") from exc


def explain_prediction(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate SHAP explanation for a single patient prediction.

    Returns
    -------
    dict with keys: feature_importance (sorted), base_value, expected_class
    """
    try:
        explainer = _get_explainer()
        X = build_feature_vector(patient_data)
        shap_values = explainer.shap_values(X)

        severity, _, _ = predict_severity(patient_data)
        feature_names = get_feature_names()

        # shap_values is list[ndarray] for multi-class; pick predicted class
        if isinstance(shap_values, list):
            class_shap = shap_values[severity][0]
        else:
            class_shap = shap_values[0]

        importance = sorted(
            zip(feature_names, class_shap.tolist()),
            key=lambda x: abs(x[1]),
            reverse=True,
        )

        summary = {
            "predicted_class": severity,
            "predicted_label": settings.ai.SEVERITY_CLASSES.get(severity, "Unknown"),
            "feature_importance": [
                {"feature": f, "shap_value": round(v, 4)} for f, v in importance
            ],
        }
        logger.debug("SHAP explanation: %s", summary)
        return summary
    except AIModelError:
        raise
    except Exception as exc:
        logger.exception("SHAP explanation failed")
        raise AIModelError(f"Explanation failed: {exc}") from exc


def reload_model() -> None:
    """Force-reload the model from disk (useful after retraining)."""
    global _model, _explainer
    _model = None
    _explainer = None
    _load_model()
    logger.info("Model reloaded from disk")
