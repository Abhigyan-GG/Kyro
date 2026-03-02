Perfect. I’ll give you a **single structured `.md` file** that contains:

1. ✅ Complete parameter checklist for improving model accuracy
2. ✅ Exact dataset structure (what columns must exist)
3. ✅ Feature engineering blueprint
4. ✅ Synthetic data generation prompt (for Claude)
5. ✅ Model evaluation script (F1, Recall, R² if regression)
6. ✅ Clear emergency-specialized modeling strategy

You can save this as:

```bash
emergency_severity_model_blueprint.md
```

---

# 📄 `emergency_severity_model_blueprint.md`

````md
# TRIAGE-AI — Emergency Severity Model Blueprint

This document defines:

1. Complete parameter list for model accuracy improvement
2. Dataset schema
3. Feature engineering strategy
4. Synthetic data generation prompt
5. Model training & evaluation script (F1 / Recall / R²)

---

# 1️⃣ Objective

Build an emergency-specialized severity prediction model using XGBoost.

Target:
Multi-class classification

0 = Low
1 = Medium
2 = High
3 = Critical

Primary evaluation metric:
F1-score (macro + weighted)
Recall for Critical class

---

# 2️⃣ Dataset Structure

The dataset must include the following structured columns:

## A. Demographics

- patient_id
- age
- gender

## B. Vital Signs (Most Important)

- heart_rate
- systolic_bp
- diastolic_bp
- respiratory_rate
- oxygen_saturation
- temperature
- gcs_score

## C. Engineered Emergency Indicators

- shock_index (heart_rate / systolic_bp)
- mean_arterial_pressure
- hypoxia_flag
- hypotension_flag
- tachycardia_flag
- fever_flag
- hypertensive_crisis_flag

## D. Symptoms (Binary Multi-Hot Encoding)

- chest_pain
- shortness_of_breath
- altered_consciousness
- trauma
- stroke_symptoms
- seizure
- severe_bleeding
- abdominal_pain
- high_fever
- severe_headache

## E. Comorbidities (Binary)

- diabetes
- hypertension
- cardiac_disease
- copd
- kidney_disease
- cancer
- immunosuppressed

## F. Target Column

- severity_class

---

# 3️⃣ Parameters That Increase Model Accuracy

## Data-Level Improvements

- Balanced class distribution
- Remove extreme outliers
- Normalize numerical features
- Encode categorical properly
- Add engineered features
- Handle missing values explicitly
- Add interaction terms

---

## Feature Engineering Enhancements

Compute:

shock_index = heart_rate / systolic_bp

mean_arterial_pressure =
(2 * diastolic_bp + systolic_bp) / 3

Binary flags:

hypoxia_flag = oxygen_saturation < 92
tachycardia_flag = heart_rate > 100
hypotension_flag = systolic_bp < 90
fever_flag = temperature > 38
hypertensive_crisis_flag = systolic_bp > 180

These drastically improve emergency accuracy.

---

## XGBoost Hyperparameters

Use grid search over:

max_depth: 4–8
learning_rate: 0.01–0.1
n_estimators: 200–500
subsample: 0.7–1.0
colsample_bytree: 0.7–1.0
gamma: 0–5
lambda (L2)
alpha (L1)

---

## Training Strategy

- Use stratified train-test split
- Apply cross-validation
- Tune for recall of class 3
- Use class weights
- Early stopping rounds

---

# 4️⃣ Synthetic Data Generation Prompt (For Claude)

Use this prompt to generate realistic synthetic emergency dataset:

---

You are generating synthetic emergency department data.

Generate 5000 patient records in CSV format with the following columns:

age (0–95)
gender (Male/Female)
heart_rate (40–180)
systolic_bp (70–220)
diastolic_bp (40–120)
respiratory_rate (10–40)
oxygen_saturation (70–100)
temperature (34–41)
gcs_score (3–15)

Binary symptom columns:
chest_pain
shortness_of_breath
altered_consciousness
trauma
stroke_symptoms
seizure
severe_bleeding
abdominal_pain
high_fever
severe_headache

Binary comorbidity columns:
diabetes
hypertension
cardiac_disease
copd
kidney_disease
cancer
immunosuppressed

Generate severity_class based on realistic emergency rules:

Critical if:
- oxygen_saturation < 85
- systolic_bp < 80
- gcs_score < 8
- severe_bleeding = 1

High if:
- shock_index > 1
- chest_pain + cardiac_disease
- stroke_symptoms = 1

Medium otherwise.

Return as structured CSV.

---

# 5️⃣ Model Training & Evaluation Script

Save as:

evaluate_model.py

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score, r2_score
from xgboost import XGBClassifier

# Load dataset
df = pd.read_csv("synthetic_emergency_data.csv")

# Feature engineering
df["shock_index"] = df["heart_rate"] / df["systolic_bp"]
df["mean_arterial_pressure"] = (
    2 * df["diastolic_bp"] + df["systolic_bp"]
) / 3

X = df.drop(columns=["severity_class"])
y = df["severity_class"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Model
model = XGBClassifier(
    objective="multi:softprob",
    num_class=4,
    max_depth=6,
    learning_rate=0.05,
    n_estimators=300,
    subsample=0.8,
    colsample_bytree=0.8
)

model.fit(X_train, y_train)

# Predictions
y_pred = model.predict(X_test)

print("F1 Score (Macro):", f1_score(y_test, y_pred, average="macro"))
print("F1 Score (Weighted):", f1_score(y_test, y_pred, average="weighted"))

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))
````

---

# 6️⃣ If Using Regression Instead

If predicting ICU probability:

Use:

XGBRegressor

Then compute:

```python
r2_score(y_test, y_pred)
```

---

# 7️⃣ Model Validation Strategy

Evaluate:

* Accuracy
* Macro F1
* Weighted F1
* Recall (Critical class)
* Confusion matrix
* ROC curve

Important:
Minimize false negatives for severity_class = 3

---

# 8️⃣ Summary

To maximize emergency response accuracy:

• Use strong vitals
• Engineer shock-related features
• Use XGBoost
• Tune hyperparameters
• Focus on Recall for Critical
• Use balanced dataset
• Evaluate with F1, not just accuracy

---

END OF DOCUMENT

```
