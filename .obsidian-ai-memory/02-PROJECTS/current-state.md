# Current State

_Last scanned: 2026-05-21 (layered architecture Phase 1–2)._

## Stack

- **Languages**: TypeScript (apps/web), Python 3.10+ (services/*, packages/scoring/)
- **Frameworks**: Next.js 14.2.35 (app router), FastAPI 0.115, SQLAlchemy 2.0, Pydantic v2, Celery 5.4
- **Package Manager**: pnpm 9 (JS workspaces); pip per service
- **Databases**: PostgreSQL 16 (Docker dev), SQLite (local fallback)
- **Queue**: Redis 7 + Celery

## Infrastructure

- **Docker**: `docker compose up -d --build` — postgres, redis, core-api, core-worker, ats-engine, ai-rewriter, resume-parser
- **Dev web**: `pnpm dev` from repo root → http://localhost:3000
- **API**: http://localhost:8000 — `AUTO_CREATE_TABLES=true` in compose for local dev

## Architecture refactor (in progress)

**Standard:** layered domain modules — see `.obsidian-ai-memory/05-ARCHITECTURE/layered-modules.md`

| Phase | Status |
|-------|--------|
| 1 Folder scaffold (core-api + apps/web/modules) | Done |
| 2 Auth (`/auth/register`, `/auth/login`) | Done |
| 3 Profile (`GET/PUT /profile`) | Done |
| 4 Resume + export | **Next** |
| 5–7 ATS, dashboard, frontend, satellites | Pending |

**Legacy still active:** most routes in `services/core-api/app/main.py`; ORM in `models/entities.py`.

## Frontend (apps/web)

- **Shell**: Sticky `AppHeader` — Overview (hero) + Workspace (student console)
- **Hero / workspace tabs**: unchanged
- **Module folders**: `apps/web/modules/{auth,profile,resume,ats,dashboard,officer}/` scaffolded (not wired yet)
- **Styling**: CSS variables in `globals.css` — no Tailwind
- **Docs**: `05-ARCHITECTURE/frontend-ux.md`, `05-ARCHITECTURE/layered-modules.md`

## Backend highlights

- **Layered auth + profile:** `api/controllers/auth_controller.py`, `profile_controller.py` → handlers/query → repos/views
- Resume upload + parse via `services/resume-parser` (routes still in `main.py`)
- Role auth on core-api (student/officer/admin)
- Alembic migration `0002_campus_ai_schema`
- JWT/crypto helpers remain in `app/services/auth.py` (not duplicated in handlers)

## Verification (last known)

| Check | Result |
|---|---|
| `tsc --noEmit` (apps/web) | pass (2026-05-20; re-run after frontend module moves) |
| core-api import + `/auth/*` routes | pass (2026-05-21) |
| Python AST parse (core-api/app) | pass (2026-05-21) |

## What's blocked

- Match engine service (Week 2)
- Officer dashboard route group (Week 4)
- `packages/scoring/` shared formula package (pending)
- Remaining core-api domains not yet extracted from `main.py`

---
_Updated: 2026-05-21 — layered architecture scaffold + auth migration; vault synced._
