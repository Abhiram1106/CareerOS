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

## Core-API internal layout (layered refactor — 2026-05-21)

**Vault:** `.obsidian-ai-memory/05-ARCHITECTURE/layered-modules.md`  
**Phases:** auth + profile migrated; resume/ats/dashboard still in `main.py`.

```
services/core-api/app/
  main.py              — legacy routes + include_router(api_router)
  api/
    router.py
    controllers/
      auth_controller.py   # DONE: /auth/register, /auth/login
      profile_controller.py  # DONE: GET/PUT /profile
  modules/
    <domain>/mutation|query|dto|mapper|types/
  adapter/db/persistence/<domain>/*.repo.py | *.view.py
  models/entities.py   — ORM (split to adapter/db/entities/ later)
  schemas/contracts.py — DTOs; auth types from modules/auth/dto/
  services/
    auth.py            — JWT + password crypto only (not route logic)
    clients.py
    pdf_export.py
  workers/
  templates/
```

## FastAPI conventions (strict)

- **Migrated domain:** controller → handler (write) or query service (read) → repo/view.
- **Unmigrated domain:** thin route in `main.py` → delegate to `app/services/` until moved.
- **Never** SQL or business rules in controllers.
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
