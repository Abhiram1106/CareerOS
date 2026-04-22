# Backend

This folder contains all backend code and backend-related assets:
- `platform/` microservices and infra
- `ATS/` NEXUS ATS service and ATS blueprint sources
- `docs/` product and roadmap docs
- `legacy/` older monolith prototype
- External access is exposed only through Core API on port `8000`

## Run Entire Backend

```bash
cd C:/Users/ADMIN/Desktop/CareerOS/backend
docker compose up --build
```

This uses `backend/docker-compose.yml` (root-level backend compose).
Before first run, apply migrations in `platform/services/core-api`:

```bash
alembic upgrade head
python scripts/seed_dev_data.py
```

## Stop

```bash
cd C:/Users/ADMIN/Desktop/CareerOS/backend
docker compose down
```

Core API docs: http://localhost:8000/docs
All other backend services are internal-only (not published on host ports).
