# Backend Context — CareerOS Student AI
# @include this file when working in any `services/*` directory

## Service map

| Service | Port | Purpose |
|---|---:|---|
| `services/core-api` | 8000 | FastAPI orchestrator (auth, resumes, ATS, scoring, jobs, assistant) |
| `services/ats-engine` | 8001 | Rule-based ATS parse-safety scorer |
| `services/ai-rewriter` | 8003 | Proof-linked resume rewrite suggestions |
| `services/resume-parser` | 8004 | PDF/DOCX to structured section JSON |
| `services/match-engine` | 8005 | JD matching (TF-IDF + semantic) |
| `services/jobs-feed` | 8006 | Jobs ingestion + cache + seed fallback |

## Access model

- Student runtime only.
- `require_student` is the application gate.
- Non-student roles are rejected at login.

## Core architecture

- Controllers in `app/api/controllers/`
- Business handlers in `app/modules/*/mutation`
- Read services in `app/modules/*/query`
- Persistence adapters in `app/adapter/db/persistence/*`
- Shared infra in `app/services/*` and `app/middleware/*`

## Security guardrails

- Strict DTO validation (`extra=forbid`)
- IDOR protection on user-owned resources
- Security headers + rate limiting
- Prompt-injection guards in assistant
- Audit events for key actions

## Migration baseline

- Alembic starts from `0001_student_baseline.py`.
- No legacy non-student schema branches remain.
