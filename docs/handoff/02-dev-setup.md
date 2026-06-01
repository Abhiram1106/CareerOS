# 02 — Dev Setup

## Prerequisites

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Node.js 20+ and pnpm 9: `npm install -g pnpm@9`
- Python 3.11+ (only needed if running scoring tests locally)
- Git

---

## Clone and start

```bash
git clone <repo-url> CareerOS
cd CareerOS

# Start all 9 backend containers (builds images on first run, ~5-10 min)
docker compose up -d --build

# Start frontend dev server (separate terminal)
cd apps/web
pnpm install
pnpm dev
```

Open http://localhost:3000 — you should see the login page.
Open http://localhost:8000/docs — FastAPI Swagger UI.

---

## Verify everything is healthy

```bash
docker compose ps
# All 9 services should show "healthy" or "Up"

curl http://localhost:8000/ready
# {"status":"ready","database":"ok"}
```

---

## Create a test account

```bash
curl -s -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"you@test.com","password":"Test123!","full_name":"Your Name"}'
```

---

## Environment files

**Backend** — `services/core-api/.env` (create from `.env.example`):
```
DATABASE_URL=postgresql://careeros:careeros@localhost:5432/careeros
REDIS_URL=redis://localhost:6379
JWT_SECRET=change-this-in-production
```

**Frontend** — `apps/web/.env.local` (already exists):
```
NEXT_PUBLIC_CORE_API_URL=http://localhost:8000
```

**Optional — Adzuna jobs API:**
```
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key
```
Without these, job search uses 12 seeded jobs — fine for dev.

---

## Stopping and cleaning up

```bash
# Stop all containers (data preserved)
docker compose down

# Stop + wipe all data (full reset)
docker compose down -v

# Rebuild a single service after code changes
docker compose build core-api && docker compose up -d core-api
```

---

## Docker data location

All Docker images and containers are stored at:
```
E:\DockerData\DockerDesktopWSL\disk\docker_data.vhdx
```
(Configured in Docker Desktop settings — not C: drive.)

---

## Running tests

```bash
# Discrimination gate (scoring unit test) — runs inside core-api container
docker compose cp tests/golden/corpus.py core-api:/tmp/corpus.py
docker compose cp tests/golden/_runner.py core-api:/tmp/_runner.py
docker compose exec core-api python /tmp/_runner.py

# TypeScript typecheck
cd apps/web && npx tsc --noEmit

# Python AST parse (syntax check all services)
find services packages -name "*.py" | xargs python -c "import ast,sys;[ast.parse(open(f).read()) for f in sys.argv[1:]]"
```

---

## Common issues

| Problem | Fix |
|---|---|
| `docker compose up` fails on Windows | Start Docker Desktop first, wait for the whale icon to stop animating |
| Port 3000 already in use | `netstat -ano \| findstr :3000` then `taskkill /F /PID <pid>` |
| `pnpm install` fails | Ensure Node 20+: `node --version` |
| core-api unhealthy | Check logs: `docker compose logs core-api --tail=50` |
| match-engine slow to start | Normal — loads MiniLM model (~2–3 seconds) |
| Alembic migration needed | Run via Docker: `docker compose exec core-api alembic upgrade head` |

---

## Intel benchmark (optional)

To generate real performance numbers:
```bash
docker compose exec match-engine python -c "
from services.intel_bench.workloads.embedding_minilm import benchmark_embedding_compare
import json; print(json.dumps(benchmark_embedding_compare(), indent=2))
"
```
Results appear in `docs/benchmarks/benchmark_runs.json`.
