# Database Context — CareerOS Campus AI
# @include this file when working with Alembic, entities, or schema changes

## Schema (as of 0002_campus_ai_schema)

### Core auth
| Table | Key columns |
|---|---|
| `users` | id, email, password_hash, full_name, role (student\|officer\|admin) |
| `session_tokens` | id, token, user_id, is_active |
| `career_profiles` | id, user_id (1:1), city, target_role, skills_csv, summary |

### Resume
| Table | Key columns |
|---|---|
| `resumes` | id, user_id, template_name, content_text, file_uri, source_format |
| `resume_sections` | id, resume_id, section_name, content_json (Text), confidence |
| `resume_evidence` | id, resume_id, claim_id, proof_uri, verified_by, status |
| `resume_export_jobs` | id, user_id, resume_id, status, file_path |

### Institutional
| Table | Key columns |
|---|---|
| `colleges` | id, name, state, college_type |
| `departments` | id, college_id, name |
| `batches` | id, college_id, dept_id, created_by, name, grad_year |
| `batch_resumes` | id, batch_id, resume_id, status (unique: batch+resume) |

### JD + Scoring
| Table | Key columns |
|---|---|
| `job_descriptions` | id, college_id, created_by, company, role, raw_text, skills_json, eligibility_json |
| `scorecards` | id, resume_id, jd_id, jd_match, ats_safety, evidence_quality, profile_completeness, interview_readiness, placement_hygiene, overall_score, bucket |
| `recommendations` | id, scorecard_id, rec_type, section, before_text, after_text, evidence_ids, confidence, accepted |

### Audit + Intel
| Table | Key columns |
|---|---|
| `events_audit` | id, actor_id, action, target_type, target_id, payload_json, ts |
| `benchmark_runs` | id, workload, dataset_size, baseline_ms, intel_ms, throughput_rph, accuracy_delta |
| `ats_scans` | id, user_id, composite_score, keyword_score, … (legacy, kept for backward compat) |

## Adding a new table — exact steps

1. Add SQLAlchemy model to `services/core-api/app/models/entities.py` (mapped-column style)
2. Write migration: `alembic revision -m "add <table>"`
3. Review autogenerate output — always verify before applying
4. Test cycle: `alembic upgrade head` → `alembic downgrade base` → `alembic upgrade head`
5. Update `05-ARCHITECTURE/README.md` schema section

## JSON columns

`content_json`, `skills_json`, `eligibility_json`, `evidence_ids`, `payload_json` are stored
as `Text` for SQLite/Postgres compat during development.

Serialize with `json.dumps()` before storing; deserialize with `json.loads()` when reading.
Migration to `JSONB` with Postgres indexing planned for Week 2 when skill extraction lands.

## Alembic file locations

- Config: `services/core-api/alembic.ini`
- Env: `services/core-api/migrations/env.py`
- Versions: `services/core-api/migrations/versions/`
  - `0001_initial.py` — baseline (users, session_tokens, career_profiles, resumes, ats_scans, resume_export_jobs)
  - `0002_campus_ai_schema.py` — Campus AI tables + role column on users

## NEVER do this

- Do not modify `entities.py` without a corresponding Alembic migration
- Do not use `AUTO_CREATE_TABLES=true` in production
- Do not add SQLAlchemy `create_all()` anywhere — migrations only
- Do not add PII to `events_audit.payload_json` — entity IDs only
