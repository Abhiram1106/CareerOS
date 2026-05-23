---
tags: [project, snapshot, verification]
type: project
updated: 2026-05-23
links: [_INDEX, architecture-index, session-index]
---

# Current State

← [[_INDEX]] · [[architecture-index]]

_Last scanned: 2026-05-23 (Week 2 complete + audit hardening)._

> **Latest:** Week 2 demo loop is live end-to-end (resume → JD parse → match → score → readiness UI). P0/P1 audit items closed: RBAC on student routes, honest `semantic_method` labelling, persisted `ats_flags` + `college_id`, golden-path API test, hardened formula tests, deleted legacy panes/AppHeader stack.

## Stack

- **Languages**: TypeScript strict (apps/web), Python 3.10+ (services/*, packages/scoring/)
- **Frameworks**: Next.js 14.2.35 (app router), FastAPI 0.115, SQLAlchemy 2.0, Pydantic v2, Celery 5.4
- **Package Manager**: pnpm 9 (JS workspaces); pip per service
- **Databases**: PostgreSQL 16 (Docker dev), SQLite (local fallback + tests)
- **Queue**: Redis 7 + Celery

## Infrastructure

- **Docker**: `docker compose up -d --build` — postgres, redis, core-api, core-worker, ats-engine, ai-rewriter, resume-parser, **match-engine**
- **Dev web**: `pnpm dev` from repo root → http://localhost:3000
- **API**: http://localhost:8000 — `AUTO_CREATE_TABLES=true` in compose for local dev

## Architecture refactor

**Standard:** layered domain modules — see [[05-ARCHITECTURE/layered-modules]]

| Phase | Status |
|-------|--------|
| 1 Folder scaffold (core-api + apps/web/modules) | Done |
| 2 Auth (`/auth/register`, `/auth/login`) | Done |
| 3 Profile (`GET/PUT /profile`) | Done |
| 4 Resume + export | Done |
| 5 ATS parse-safety (engine narrowed; legacy `/scan` removed) | Done |
| 6 JD parsing + match-engine + scorecard | Done |
| 7 Officer dashboard, frontend full-cutover, satellites | In progress (Week 4) |

**Legacy still active:** some routes in `services/core-api/app/main.py`; ORM in `models/entities.py`.

## Frontend (apps/web)

- **Shell**: `app/(app)/layout.tsx` builds nav inline (role-aware: student vs officer)
- **Workspace**: `app/(app)/workspace/page.tsx` driven by single `usePlacementWorkspace` hook
  - Tabs: Document Intelligence · JD Match Scan · Readiness Snapshot
  - `ScoreBreakdown` shows six bars + bucket badge + `semantic_method` tooltip
- **API client**: typed `apps/web/lib/api.ts` (no inline fetch in screens)
- **Module folders**: `apps/web/modules/{auth,profile,resume,ats,dashboard,officer,scorecard}/` — `scorecard/services/scorecardService.ts` ready for migration
- **Styling**: CSS variables in `globals.css` — no Tailwind
- **Cleanup (2026-05-23):** deleted orphaned `components/panes/**`, `components/SectionNav.tsx`, `components/workspace/WorkspaceTabs.tsx`, `components/layout/{AppHeader,SiteNav,AppFooter}.tsx`, `hooks/useCareerOSWorkspace.ts`

## Backend highlights

- **Layered auth + profile + resume:** controllers/handlers/query/repos/views split
- **Match engine** (`services/match-engine`): TF-IDF + char n-gram cosine (`embedding_proxy_tfidf`) + skill recall + eligibility — `sklearnex.patch_sklearn()` called before sklearn import. Honest `semantic_method` field returned on every match.
- **ATS engine** narrowed to `POST /parse-safety` only. Composite scoring removed.
- **Scoring package** (`packages/scoring/`): single source of truth for `PlacementReadinessScore`. Imported by core-api `score_resume_handler`; never inlined.
- **Scorecard repo** persists `ats_flags`, `semantic_method`, and `college_id` (from request → user fallback).
- **RBAC**: `require_student` / `require_officer` enforced on all role-specific routes.
- **Tests**: golden-path API integration test (`services/core-api/tests/test_scoring_golden_path.py`) + hardened formula unit tests (`packages/scoring/tests/test_formula.py`).

## Verification (2026-05-23)

| Check | Result |
|---|---|
| `tsc --noEmit` (apps/web) | **pass** |
| Python AST parse (core-api, ats-engine, match-engine, scoring, tests) | **pass** (107 files) |
| Golden-path API test | green |
| Formula tests (clamp, weights, buckets, ats penalty) | green |

## What's next

- Week 3: AI rewriter retargeted (proof-linked JSON-schema, no fabrication), before/after diff UI, ATS-safe PDF export
- Week 4: officer route group — batches, dept heatmap, review queue, skill-gap chart
- Week 5: `services/intel-bench` + lab panel + pitch deck
- Tech-debt: extract remaining `main.py` routes into layered modules; migrate workspace state to `modules/scorecard/hooks/`

---
_Updated: 2026-05-23 — Week 2 complete, audit hardening landed, legacy UI stack removed._

*Related: [[_INDEX]] · [[architecture-index]] · [[05-ARCHITECTURE/layered-modules]] · [[api-index]] · [[02-PROJECTS/active-goals]] · [[session-index]]*
