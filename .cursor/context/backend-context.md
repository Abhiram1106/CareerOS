# Backend Context — CareerOS Campus AI
# @include this file when working in any services/* directory

## Service map

| Service | Port | Entry | Purpose |
|---|---|---|---|
| `services/core-api` | 8000 | `app/main.py` | FastAPI orchestrator — auth, resumes, ATS, scoring |
| `services/ats-engine` | 8001 | `app/main.py` | Rule-based ATS parse-safety scorer |
| `services/ai-rewriter` | 8003 | `app/main.py` | Proof-linked resume rewriter (JSON schema output) |
| `services/resume-parser` | 8004 | `app/main.py` | PDF/DOCX → structured section JSON |
| `services/match-engine` | 8005 | `app/main.py` | TF-IDF + embeddings + skill recall (Week 2, pending) |
| `services/intel-bench` | CLI | `run.py` | OpenVINO + sklearnex benchmark harness (Week 5) |

## Core-API internal layout

```
services/core-api/app/
  main.py           — all routes (slim handlers only)
  config.py         — os.getenv() config, validated at startup
  database.py       — SQLAlchemy engine + SessionLocal + get_db
  db_bootstrap.py   — startup health gate
  dependencies.py   — current_user, require_student, require_officer, require_admin
  models/
    entities.py     — ALL SQLAlchemy 2.0 mapped-column models
  schemas/
    contracts.py    — ALL Pydantic v2 request/response schemas
  services/
    auth.py         — hash_password, verify_password, create_access_token, create_session
    clients.py      — httpx async calls to downstream services
    pdf_export.py   — WeasyPrint resume PDF export
  workers/
    celery_app.py   — Celery app config
    tasks.py        — generate_resume_export (Celery task)
  templates/        — Jinja2 HTML for PDF export
```

## FastAPI conventions (strict)

- Route handler = validate input + call service layer + return. Nothing else.
- Business logic in `services/<svc>/app/services/`, never in route functions.
- `Depends(current_user)` on all protected routes.
- `require_officer` gate on all officer-only endpoints.
- Schema changes → write Alembic migration, never rely on `entities.py` alone.

## SQLAlchemy 2.0 pattern

```python
from sqlalchemy.orm import Mapped, mapped_column
class MyModel(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
```
Never use legacy `Column()`.

## Pydantic v2 pattern

```python
from pydantic import BaseModel, Field
class MyRequest(BaseModel):
    value: str = Field(..., min_length=1)
# Use .model_dump() not .dict()
# Use .model_validate() not .parse_obj()
```

## Alembic workflow

```bash
cd services/core-api
alembic revision -m "describe change"   # create migration
alembic upgrade head                    # apply
alembic downgrade -1                    # roll back one
```
Always test upgrade + downgrade + upgrade cycle on a fresh DB.

## Cross-service calls

All cross-service HTTP in `services/core-api/app/services/clients.py` only.
Use httpx async — never requests. All URLs from config.py env vars.

## Auth tokens

JWT payload: `{"sub": user_id, "role": "student|officer|admin", "exp": ...}`
`create_access_token(user)` takes a full User model.
`get_user_by_token(db, token)` validates against session_tokens table.

## Current DB tables

Initial: users, session_tokens, career_profiles, resumes, ats_scans, resume_export_jobs
Week 1 (0002): colleges, departments, resume_sections, resume_evidence,
               job_descriptions, scorecards, recommendations,
               batches, batch_resumes, events_audit, benchmark_runs
