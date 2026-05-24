# Database Context — CareerOS Student AI
# @include when editing Alembic, entities, or persistence code

## Baseline migration

- `services/core-api/migrations/versions/0001_student_baseline.py`
- Single baseline for fresh environments.
- No non-student tables or legacy branch migrations.

## Core table groups

- Auth/session: `users`, `session_tokens`
- Student profile/resume: `career_profiles`, `resumes`, `resume_sections`, `resume_evidence`, `resume_export_jobs`, `ats_scans`
- Scoring pipeline: `job_descriptions`, `scorecards`, `recommendations`
- Job and orchestration: `jobs`, `agent_runs`
- Audit and benchmark: `events_audit`, `benchmark_runs`

## Migration rules

1. Update SQLAlchemy models.
2. Add Alembic migration.
3. Validate upgrade/downgrade cycle.
4. Keep migrations aligned with student-only scope.

## Guardrails

- Do not reintroduce non-student tables.
- Do not rely on `create_all()` for production.
- Do not store sensitive PII in `events_audit.payload_json`.
