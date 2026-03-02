import pandas as pd
import numpy as np

print("Loading dataset...")
df = pd.read_csv("ed2022.csv", low_memory=False)

# -----------------------------
# Select Important Columns
# -----------------------------

columns_needed = [
    "AGE", "SEX", "RACERETH",
    "TEMPF", "PULSE", "RESPR", "BPSYS", "BPDIAS",
    "PAINSCALE", "IMMEDR",
    "ADMITHOS", "ADMIT", "DIEDED", "LOS",
    "ASTHMA", "CANCER", "CKD", "COPD",
    "CHF", "CAD", "DIABTYP1", "DIABTYP2",
    "HTN", "OBESITY"
]

df = df[columns_needed]

# -----------------------------
# Rename Columns
# -----------------------------

df = df.rename(columns={
    "AGE": "age",
    "SEX": "gender",
    "TEMPF": "temperature",
    "PULSE": "heart_rate",
    "RESPR": "respiratory_rate",
    "BPSYS": "systolic_bp",
    "BPDIAS": "diastolic_bp",
    "PAINSCALE": "pain_scale",
})

# -----------------------------
# Remove Impossible Vitals
# -----------------------------

df = df[
    (df["heart_rate"].between(30, 220)) &
    (df["systolic_bp"].between(60, 250)) &
    (df["diastolic_bp"].between(30, 150)) &
    (df["temperature"].between(90, 110))
]

df = df.dropna(subset=[
    "heart_rate", "systolic_bp",
    "diastolic_bp", "temperature"
])

# -----------------------------
# Feature Engineering
# -----------------------------

df["shock_index"] = df["heart_rate"] / df["systolic_bp"]

df["mean_arterial_pressure"] = (
    2 * df["diastolic_bp"] + df["systolic_bp"]
) / 3

df["tachycardia_flag"] = (df["heart_rate"] > 100).astype(int)
df["hypotension_flag"] = (df["systolic_bp"] < 90).astype(int)
df["fever_flag"] = (df["temperature"] > 100.4).astype(int)

# -----------------------------
# Severity Label Creation
# -----------------------------

def assign_severity(row):
    if row["DIEDED"] == 1:
        return 3
    if row["IMMEDR"] == 1:
        return 3
    if row["ADMITHOS"] == 1:
        return 2
    if row["shock_index"] > 1:
        return 1
    return 0

df["severity_class"] = df.apply(assign_severity, axis=1)

# -----------------------------
# Drop raw outcome columns
# -----------------------------

df = df.drop(columns=[
    "IMMEDR", "ADMITHOS", "ADMIT", "DIEDED"
])

# -----------------------------
# Save Clean Dataset
# -----------------------------

df.to_csv("dataset.csv", index=False)

print("Dataset created successfully.")
print("Shape:", df.shape)
print(df["severity_class"].value_counts())