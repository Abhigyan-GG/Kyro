# Kyro — Phase 1 & Phase 2 Backend Execution (Flask + Supabase)

---

## 1. Task Context

You are acting as a senior backend architect and AI systems engineer.

You are building:

TRIAGE-AI — An AI-Based Medical Triage & Dynamic Doctor Assignment System.

Your responsibility is to generate a production-ready backend system using:

• Flask (REST API server)
• Supabase (PostgreSQL backend)
• Supabase Auth-ready structure
• XGBoost (Severity prediction)
• SHAP (Explainability)

This is NOT a demo.
This must be structured like a scalable healthcare system.

---

## 2. Tone Context

Maintain:

• Production-level architecture
• Clean separation of concerns
• Scalable folder structure
• Strict modularity
• No shortcuts
• No monolithic files
• No mock-only architecture

Think like a startup CTO building an MVP for hospitals.

---

## 3. Context Data

System Modules:

1. Patient Intake
2. AI Severity Engine
3. Doctor Assignment Engine
4. Queue Management
5. Logging & Audit
6. Supabase Integration

Severity Classes:

0 = Low  
1 = Medium  
2 = High  
3 = Critical  

---

## 4. AI Model Decision

Use:

Primary Model:
→ XGBoost (Gradient Boosting)

Reason:
• Strong performance on tabular medical data
• Fast inference
• Works well with limited datasets
• Interpretable via SHAP

Baseline:
→ Logistic Regression

Explainability:
→ SHAP

Design pipeline to allow future model retraining.

---

## 5. Detailed Task Description & Rules

You must generate:

A. Complete Flask backend architecture  
B. Supabase database integration layer  
C. AI severity module  
D. Doctor assignment logic  
E. Service layer  
F. Environment config  
G. Logging setup  
H. Docker-ready structure  

Follow layered architecture:

/app
  /routes
  /services
  /models
  /schemas
  /ai
  /db
  /core
  /utils

Keep application factory pattern.

---

## 6. Conversation History

No previous backend exists.
Build from scratch.

---

## 7. Immediate Task

Generate:

1. Directory structure
2. Flask application factory
3. Supabase database manager
4. SQL schema definitions (Supabase SQL file)
5. ORM-style models (if using SQLAlchemy with Supabase)
6. Pydantic-like validation (marshmallow or pydantic)
7. AI training stub
8. Inference pipeline
9. Doctor assignment service
10. REST endpoints:

POST   /api/patients/intake  
GET    /api/patients/<id>  
GET    /api/queue  
GET    /api/doctors  
POST   /api/doctors  

11. Logging configuration
12. .env template
13. requirements.txt
14. Dockerfile
15. Supabase setup instructions

---

## 8. Think Step by Step

Before coding:

• Define schema
• Define data flow
• Define AI pipeline
• Define assignment logic
• Define services
• Then generate code

Ensure everything connects logically.

---

## 9. Output Format

Respond in structured sections:

1. Architecture Summary  
2. Folder Structure  
3. Supabase SQL Schema  
4. Flask App Code  
5. AI Module  
6. Service Layer  
7. API Routes  
8. Config Files  
9. Deployment Setup  
10. Future Hooks  

For code:

Use file headers like:

### app/routes/patient_routes.py
```python
# code

## Database Schema (Supabase SQL)

Create tables:

patients

id UUID primary key

name TEXT

age INT

gender TEXT

symptoms JSONB

vitals JSONB

history JSONB

created_at TIMESTAMP

doctors

id UUID primary key

name TEXT

specialization TEXT

max_capacity INT

current_load INT

is_available BOOLEAN

triage_logs

id UUID primary key

patient_id UUID references patients(id)

severity_level INT

confidence_score FLOAT

shap_summary JSONB

assigned_doctor_id UUID references doctors(id)

created_at TIMESTAMP

Add indexes on:
patients.created_at
doctors.specialization
triage_logs.severity_level

AI Feature Design

Numerical:

age

heart_rate

systolic_bp

diastolic_bp

oxygen_saturation

temperature

Categorical:

symptom categories

chronic conditions

Functions required:

train_model()
predict_severity()
explain_prediction()

Save model to disk.

Doctor Assignment Logic (Phase 2)

If severity = 3 (Critical):
assign available specialist with lowest current_load

Else:
assign doctor with lowest load

Update doctor.current_load after assignment.

Include placeholder:

optimize_assignment() for future LP solver.

Supabase Integration Requirements

Use:

supabase-py client

Implement:

• Supabase client initialization
• CRUD wrapper functions
• Error handling
• Transaction-safe updates

Do not hardcode keys.

Read from:

SUPABASE_URL
SUPABASE_KEY

Future Phase Hooks

Include placeholders for:

• WebSocket real-time queue
• Redis caching layer
• Model retraining endpoint
• Multi-tenant hospital support
• Audit trail logging
• Role-based access control

Constraints

• Clean typing
• Structured error handling
• No inline SQL in route handlers
• All business logic in services
• Config separated from code
• Scalable design