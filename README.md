# Kyro — TRIAGE-AI

**AI-Based Medical Triage & Dynamic Doctor Assignment System**

A production-grade Flask backend using Supabase (PostgreSQL), XGBoost severity prediction, SHAP explainability, and dynamic doctor queue management.

---

## Architecture

```
Kyro/
├── run.py                      # Entry point
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example                # Environment template
├── supabase_schema.sql         # Database DDL
│
└── app/
    ├── factory.py              # Flask application factory
    ├── core/
    │   ├── config.py           # Typed settings from .env
    │   ├── errors.py           # Exception hierarchy
    │   └── logging.py          # Structured logging
    ├── db/
    │   └── supabase_manager.py # Supabase CRUD client
    ├── models/
    │   └── entities.py         # Domain data classes
    ├── schemas/
    │   └── validation.py       # Marshmallow request schemas
    ├── ai/
    │   ├── features.py         # Feature engineering
    │   ├── train.py            # XGBoost + LR training pipeline
    │   ├── inference.py        # Predict + SHAP explain
    │   └── artifacts/          # Saved model files
    ├── services/
    │   ├── patient_service.py  # Patient CRUD
    │   ├── doctor_service.py   # Doctor CRUD + load mgmt
    │   ├── triage_service.py   # Full triage orchestration
    │   └── queue_service.py    # Priority queue view
    ├── routes/
    │   ├── patient_routes.py   # /api/patients/*
    │   ├── doctor_routes.py    # /api/doctors/*
    │   ├── queue_routes.py     # /api/queue
    │   └── health_routes.py    # /api/health
    └── utils/
        └── helpers.py          # Response envelope, UUID, etc.
```

---

## Quick Start

### 1. Prerequisites

- Python 3.11+
- A Supabase project (free tier works)

### 2. Supabase Setup

1. Go to [supabase.com](https://supabase.com) → create a project.
2. Open the **SQL Editor**.
3. Paste the contents of `supabase_schema.sql` and run it.
4. Copy your **Project URL** and **anon/service key** from Settings → API.

### 3. Environment

```bash
cp .env.example .env
# Edit .env with your Supabase URL and Key
```

### 4. Install & Train

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

pip install -r requirements.txt

# Train the AI model (generates artifacts)
python -m app.ai.train
```

### 5. Run

```bash
python run.py
```

Server starts at `http://localhost:5000`.

---

## API Endpoints

| Method | Endpoint                  | Description                          |
|--------|---------------------------|--------------------------------------|
| GET    | `/api/health`             | Liveness check                       |
| POST   | `/api/patients/intake`    | Patient intake + AI triage           |
| GET    | `/api/patients/<id>`      | Get patient by UUID                  |
| GET    | `/api/patients`           | List recent patients                 |
| POST   | `/api/doctors`            | Register a doctor                    |
| GET    | `/api/doctors`            | List all doctors                     |
| GET    | `/api/doctors/<id>`       | Get doctor by UUID                   |
| GET    | `/api/queue`              | Severity-prioritised triage queue    |

### Example: Patient Intake

```bash
curl -X POST http://localhost:5000/api/patients/intake \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "age": 65,
    "gender": "male",
    "symptoms": [
      {"category": "cardiac", "description": "chest pain"}
    ],
    "vitals": {
      "heart_rate": 110,
      "systolic_bp": 160,
      "diastolic_bp": 95,
      "oxygen_saturation": 93,
      "temperature": 37.2
    },
    "history": {
      "chronic_conditions": ["hypertension", "diabetes"]
    }
  }'
```

### Example: Register a Doctor

```bash
curl -X POST http://localhost:5000/api/doctors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. Smith",
    "specialization": "cardiology",
    "max_capacity": 8
  }'
```

---

## Severity Classes

| Level | Label    | Description                  |
|-------|----------|------------------------------|
| 0     | Low      | Non-urgent, routine          |
| 1     | Medium   | Needs attention soon         |
| 2     | High     | Urgent, priority care        |
| 3     | Critical | Immediate intervention       |

---

## Docker

```bash
docker compose up --build
```

---

## Future Phase Hooks

- [ ] WebSocket real-time queue updates
- [ ] Redis caching layer
- [ ] Model retraining endpoint (`POST /api/ai/retrain`)
- [ ] Multi-tenant hospital support
- [ ] Audit trail logging (table exists)
- [ ] Role-based access control (Supabase Auth)
- [ ] LP-based assignment optimization

---

## Tech Stack

| Component       | Technology               |
|-----------------|--------------------------|
| API Server      | Flask 3.x                |
| Database        | Supabase (PostgreSQL)    |
| AI Model        | XGBoost                  |
| Baseline        | Logistic Regression      |
| Explainability  | SHAP                     |
| Validation      | Marshmallow              |
| Production WSGI | Gunicorn                 |
| Container       | Docker                   |

---

*Built by Kyro — Phase 1 & Phase 2*
