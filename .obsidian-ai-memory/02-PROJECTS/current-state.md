---
tags: [project, snapshot, verification, security]
type: project
updated: 2026-05-23
links: [_INDEX, architecture-index, session-index, security-architecture]
---

# Current State

← [[_INDEX]] · [[05-ARCHITECTURE/security-architecture]]

_Last scanned: 2026-05-23 (student-first pivot complete; Kirito security roadmap defined)._

> **Latest:** Jobs feed + deterministic agent + Builder/Jobs UI shipped. RBAC on student routes. **Next:** Phase 4 officer dashboard **blocked on security gate** (IDOR, OpenAPI export, rate limits, audit).

## Stack

- **Languages**: TypeScript strict (apps/web), Python 3.10+ (services/*, packages/scoring/)
- **Frameworks**: Next.js 14.2.35, FastAPI 0.115, SQLAlchemy 2.0, Pydantic v2, Celery
- **Package Manager**: pnpm 9; pip per service
- **Databases**: PostgreSQL 16, Redis 7
- **Security (baseline)**: JWT + RBAC; Pydantic validation; proof-linked rewriter; officer flags off

## Infrastructure

- **Docker**: postgres, redis, core-api, core-worker, ats-engine, ai-rewriter, resume-parser, match-engine, **jobs-feed**
- **Web**: http://localhost:3000 · **API**: http://localhost:8000 (`/docs` OpenAPI)

## Product surfaces

| Surface | Status |
|---------|--------|
| Student workspace (manual tabs) | Live |
| Jobs Feed + Builder + agent | Live |
| Officer dashboard | Code exists; `ENABLE_OFFICER_SURFACE=false` |
| Intel lab panel | Planned (Phase 5) |
| Campus assistant | Planned (Phase 6) |

## Backend highlights

- Agent state machine: `POST /agent/run`, `GET /agent/runs/{id}`
- Tables: `jobs`, `agent_runs` (migration `0003`)
- Match-engine sklearnex benchmark documented
- Scoring: `packages/scoring/` only

## Security posture

| Control | Status |
|---------|--------|
| JWT + role guards | Implemented |
| Resource ownership (IDOR) | **Phase 4 required** |
| OpenAPI committed export | **Phase 4 required** |
| Rate limiting | **Phase 4 required** |
| TLS / prod secrets | **Phase 5 required** |
| Assistant isolation | **Phase 6 required** |

Full plan: [[05-ARCHITECTURE/security-architecture]] · `docs/security/threat-model.md`

## Verification (2026-05-23)

| Check | Result |
|-------|--------|
| `tsc --noEmit` (apps/web) | pass |
| Agent golden-path test | pass |
| Scoring golden-path test | pass |

## What's next

1. Phase 4 product: officer routes + cohort UI  
2. Phase 4 security gate: must complete before officer GA  
3. Phase 5: intel-bench + `/lab/intel`  
4. Phase 6: RAG assistant + optional LLM  

→ [[02-PROJECTS/active-goals]] · [[MASTER_PLAN]]
