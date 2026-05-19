# Current State

_Last scanned: 2026-05-19 (post Phase 2)._

## Stack

- **Languages**: TypeScript (apps/web), Python 3.10+ (services/*, packages/scoring/)
- **Frameworks**: Next.js 14.2.15 (app router), FastAPI 0.115, SQLAlchemy 2.0 (mapped-column style), Pydantic v2, Celery 5.4
- **Package Manager**: pnpm 9 (JS workspaces); pip per service
- **Test Runner**: none yet — adding alongside Week 2
- **Databases**: PostgreSQL 16 (prod), SQLite (dev fallback)
- **Queue**: Redis 7 + Celery
- **PDF Export**: WeasyPrint 62.3 (disabled on Windows native by default)

## Infrastructure

- **Docker**: yes — `docker-compose.yml` at repo root brings up Postgres, Redis, core-api, core-worker, ats-engine, ai-rewriter
- **Kubernetes**: no
- **GitHub Actions**: no — first workflow lands Week 1

## AI tooling installed

- **Claude Code** — project config at `.claude/` (settings.json, CLAUDE.md, rules/, agents/, skills/, .mcp.json) + root `CLAUDE.md`
- **Cursor** — project rules at `.cursor/rules/` (backend, frontend, project-rules, security, testing)
- **Omnix** — runtime at `.omnix/`, memory vault at `.obsidian-ai-memory/`, committed config home at `platform/omnix/` (placeholder while Omnix tooling still expects `.omnix/`)

## Monorepo layout

```
apps/web/                            (Next.js 14 — student surface; officer surface comes Week 4)
packages/{contracts,scoring,ts-types,frontend,backend}/   (frontend + backend reserved)
services/{core-api,ats-engine,ai-rewriter}/               (resume-parser, match-engine, intel-bench come Weeks 1-5)
infra/{docker,environments}/         (skeleton)
platform/{ci,scripts,build,omnix}/   (skeleton + READMEs)
docs/{adr,architecture,pitch,benchmarks,legacy}/
tests/                                (cross-domain e2e only — empty)
```

## What's shipping

- **Pivot complete**: Campus AI positioning replaces broad "AI careers platform" pitch.
- **Restructure landed on `main`**: 4 commits (5e2b191 → c2f3432 → c327416 → 172160a → Phase 2 commit pending).
- **Tracked file count**: 71 files (pre-pivot was 131).
- **TypeScript**: `npx tsc --noEmit` clean.
- **Python**: all service files AST-parse clean.

## What's blocked

- **Real pilot data**: no college partnership yet for outcome-tracking validation. Mitigation: synthetic + small hand-labeled fixture corpus for demo; outcome-lift framed as next step in pitch.
- **OpenVINO accuracy delta**: unknown until Week 5 benchmark runs. Mitigation: fall back to FP16 if INT8 hurts match quality.

## Recoverability

`origin/archive/pre-campus-ai` branch preserves the pre-cut polished MVP
(commit `c2f3432`). All deletions on `main` are recoverable from there.

---
_Updated: 2026-05-19 by Phase 2 session._
