# CareerOS Platform Monorepo

This workspace follows the documented backend stack:
- Backend: FastAPI microservices
- Data: PostgreSQL + Redis
- Async jobs: Celery + Redis broker
- Infra: Docker Compose

## Services
- `services/core-api`: Auth, profile, resume, dashboard orchestration
- `services/ats-engine`: Resume ATS scoring service
- `services/job-intel`: Job matching service
- `services/ai-inference`: LLM-compatible content generation facade
- `../../ATS/nexus_ats`: NEXUS ATS domain service (requisitions/candidates/applications/ATS pipeline)

## Run

```bash
docker compose -f infrastructure/docker-compose.yml up --build
```

Open:
- Core API docs: http://localhost:8000/docs
- NEXUS ATS service: http://localhost:8010/docs

## Run Without Docker (Local Dev)

You can run the project without Docker by starting each service in separate terminals.

1. `backend/ATS/nexus_ats`
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

2. `backend/platform/services/ai-inference`
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8003
```

3. `backend/platform/services/ats-engine`
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

4. `backend/platform/services/job-intel`
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8002
```

5. `backend/platform/services/core-api`
```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Environment
Copy `.env.example` to `.env` in `infrastructure/` if you want to override defaults.

## Migrations (Core API)
From `services/core-api`:

```bash
alembic upgrade head
```

Current implementation keeps `AUTO_CREATE_TABLES=true` for smooth bootstrap in dev/compose.
Set `AUTO_CREATE_TABLES=false` once migration-first bootstrapping is enforced in deployment.
