# Current State

_Last scanned: 2026-05-20 (enterprise frontend + run fixes)._

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

## Frontend (apps/web)

- **Shell**: Sticky `AppHeader` — Overview (hero) + Workspace (student console)
- **Hero**: Product positioning, demo loop, feature pillars, workflow steps (`components/marketing/HeroPage.tsx`)
- **Workspace tabs**: Account | Resume & ATS | Readiness (`WorkspaceTabs`)
- **Styling**: CSS variables in `globals.css` — no Tailwind
- **Docs**: `.obsidian-ai-memory/05-ARCHITECTURE/frontend-ux.md`

## Backend highlights

- Resume upload + parse via `services/resume-parser`
- Role auth on core-api (student/officer/admin)
- Alembic migration `0002_campus_ai_schema`
- Local run fixes: `python-multipart`, `bcrypt==4.0.1`, shared `export_data` volume for PDF export

## Verification (last known)

| Check | Result |
|---|---|
| `tsc --noEmit` (apps/web) | pass (2026-05-20) |
| `pnpm build` (apps/web) | pass (2026-05-20) |
| Docker compose health | pass (prior session) |

## What's blocked

- Match engine service (Week 2)
- Officer dashboard route group (Week 4)
- `packages/scoring/` shared formula package (pending)

---
_Updated: 2026-05-20 — cursor session (frontend shell + vault UX doc)._
