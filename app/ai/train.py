"""
Kyro — Model Training Pipeline

Trains an XGBoost severity classifier and saves the artefact to disk.
Also trains a Logistic Regression baseline for comparison.

Usage (standalone):
    python -m app.ai.train
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from app.ai.features import get_feature_names
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger("ai.train")


def _generate_synthetic_data(n_samples: int = 2000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic patient data for initial model training.
    Replace with real labelled data in production.
    """
    rng = np.random.RandomState(seed)

    data = {
        "age":                rng.randint(1, 100, n_samples),
        "heart_rate":         rng.normal(80, 20, n_samples).clip(30, 200),
        "systolic_bp":        rng.normal(120, 25, n_samples).clip(60, 250),
        "diastolic_bp":       rng.normal(80, 15, n_samples).clip(40, 150),
        "oxygen_saturation":  rng.normal(96, 4, n_samples).clip(60, 100),
        "temperature":        rng.normal(37.0, 1.0, n_samples).clip(34, 42),
        "symptom_category":   rng.randint(0, 8, n_samples),
        "has_chronic_condition": rng.randint(0, 2, n_samples),
    }
    df = pd.DataFrame(data)

    # Heuristic severity labels (rule-based for synthetic data)
    severity = np.zeros(n_samples, dtype=int)
    severity[df["oxygen_saturation"] < 90] = 3
    severity[(df["heart_rate"] > 130) & (severity == 0)] = 2
    severity[(df["systolic_bp"] > 180) & (severity == 0)] = 2
    severity[(df["temperature"] > 39.5) & (severity == 0)] = 2
    severity[(df["age"] > 70) & (df["has_chronic_condition"] == 1) & (severity == 0)] = 1
    severity[(df["heart_rate"] > 100) & (severity == 0)] = 1
    df["severity"] = severity

    logger.info("Synthetic dataset generated: %d samples, distribution: %s",
                n_samples, dict(zip(*np.unique(severity, return_counts=True))))
    return df


def train_model(data: pd.DataFrame | None = None) -> Tuple[XGBClassifier, LogisticRegression]:
    """
    Train XGBoost (primary) and Logistic Regression (baseline).

    Parameters
    ----------
    data : DataFrame, optional
        If None, synthetic data is generated.

    Returns
    -------
    (xgb_model, lr_model)
    """
    if data is None:
        data = _generate_synthetic_data()

    feature_cols = get_feature_names()
    X = data[feature_cols]
    y = data["severity"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )

    # --- XGBoost ---
    xgb_model = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        objective="multi:softprob",
        num_class=4,
        eval_metric="mlogloss",
        use_label_encoder=False,
        random_state=42,
    )
    xgb_model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
    xgb_preds = xgb_model.predict(X_test)
    logger.info("XGBoost classification report:\n%s",
                classification_report(y_test, xgb_preds, zero_division=0))

    # --- Logistic Regression baseline ---
    lr_model = LogisticRegression(max_iter=500, multi_class="multinomial", random_state=42)
    lr_model.fit(X_train, y_train)
    lr_preds = lr_model.predict(X_test)
    logger.info("Logistic Regression classification report:\n%s",
                classification_report(y_test, lr_preds, zero_division=0))

    # Save XGBoost model
    artifact_dir = Path(settings.ai.MODEL_PATH).parent
    artifact_dir.mkdir(parents=True, exist_ok=True)
    xgb_model.save_model(settings.ai.MODEL_PATH)
    logger.info("XGBoost model saved → %s", settings.ai.MODEL_PATH)

    # Save metadata
    meta_path = artifact_dir / "model_meta.json"
    meta = {
        "model_version": settings.ai.MODEL_VERSION,
        "features": feature_cols,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "severity_classes": settings.ai.SEVERITY_CLASSES,
    }
    meta_path.write_text(json.dumps(meta, indent=2))
    logger.info("Model metadata saved → %s", meta_path)

    return xgb_model, lr_model


# Allow direct execution: python -m app.ai.train
if __name__ == "__main__":
    from app.core.logging import setup_logging
    setup_logging()
    train_model()
