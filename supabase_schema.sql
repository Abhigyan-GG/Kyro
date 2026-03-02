-- ============================================================
-- Kyro — TRIAGE-AI  |  Supabase SQL Schema
-- Run this in the Supabase SQL Editor to bootstrap the DB.
-- ============================================================

-- Enable uuid generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- --------------------------------------------------------
-- PATIENTS
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS patients (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT        NOT NULL,
    age             INT         NOT NULL CHECK (age >= 0 AND age <= 150),
    gender          TEXT        NOT NULL CHECK (gender IN ('male', 'female', 'other')),
    symptoms        JSONB       NOT NULL DEFAULT '[]'::jsonb,
    vitals          JSONB       NOT NULL DEFAULT '{}'::jsonb,
    history         JSONB       NOT NULL DEFAULT '{}'::jsonb,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE patients IS 'Patient intake records with symptoms, vitals, and medical history.';

CREATE INDEX IF NOT EXISTS idx_patients_created_at ON patients (created_at DESC);

-- --------------------------------------------------------
-- DOCTORS
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS doctors (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name            TEXT        NOT NULL,
    specialization  TEXT        NOT NULL,
    max_capacity    INT         NOT NULL DEFAULT 10 CHECK (max_capacity > 0),
    current_load    INT         NOT NULL DEFAULT 0  CHECK (current_load >= 0),
    is_available    BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE doctors IS 'Registered doctors with capacity and availability tracking.';

CREATE INDEX IF NOT EXISTS idx_doctors_specialization ON doctors (specialization);
CREATE INDEX IF NOT EXISTS idx_doctors_available      ON doctors (is_available) WHERE is_available = TRUE;

-- --------------------------------------------------------
-- TRIAGE LOGS
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS triage_logs (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id          UUID        NOT NULL REFERENCES patients(id) ON DELETE CASCADE,
    severity_level      INT         NOT NULL CHECK (severity_level BETWEEN 0 AND 3),
    confidence_score    FLOAT       NOT NULL CHECK (confidence_score BETWEEN 0.0 AND 1.0),
    shap_summary        JSONB       NOT NULL DEFAULT '{}'::jsonb,
    assigned_doctor_id  UUID        REFERENCES doctors(id) ON DELETE SET NULL,
    model_version       TEXT        NOT NULL DEFAULT '1.0.0',
    created_at          TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE triage_logs IS 'AI triage results with severity, explainability, and doctor assignment.';

CREATE INDEX IF NOT EXISTS idx_triage_severity   ON triage_logs (severity_level);
CREATE INDEX IF NOT EXISTS idx_triage_patient     ON triage_logs (patient_id);
CREATE INDEX IF NOT EXISTS idx_triage_created_at  ON triage_logs (created_at DESC);

-- --------------------------------------------------------
-- AUDIT LOG (Future Phase — placeholder)
-- --------------------------------------------------------
CREATE TABLE IF NOT EXISTS audit_log (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actor       TEXT        NOT NULL,
    action      TEXT        NOT NULL,
    resource    TEXT        NOT NULL,
    resource_id UUID,
    metadata    JSONB       DEFAULT '{}'::jsonb,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

COMMENT ON TABLE audit_log IS 'Immutable audit trail for compliance and debugging.';

CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_log (created_at DESC);

-- --------------------------------------------------------
-- UPDATED_AT TRIGGER
-- --------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_patients_updated_at
    BEFORE UPDATE ON patients
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER trg_doctors_updated_at
    BEFORE UPDATE ON doctors
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
