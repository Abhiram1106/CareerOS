# CareerOS Student AI

Student-first placement-readiness workspace for Indian job seekers.

CareerOS helps a single user journey:

1. Upload resume
2. Parse sections
3. Run ATS parse-safety
4. Score resume against JD
5. Generate proof-linked rewrite suggestions
6. Export polished resume
7. Track jobs and run agent loop

## Scope

This repository is intentionally student-only.

- No non-student dashboards
- No institutional batch workflows
- No recruiter marketplace features

## Tech stack

- Frontend: Next.js 14 (`apps/web`)
- API: FastAPI (`services/core-api`)
- Supporting services: `resume-parser`, `ats-engine`, `ai-rewriter`, `jobs-feed`
- Data: PostgreSQL + Redis
- Worker: Celery (core worker)
- Bench: Intel/OpenVINO + sklearnex harness

## Monorepo layout

```text
apps/
  web/                  # Student UI
services/
  core-api/             # Main API and orchestration
  resume-parser/        # Resume extraction
  ats-engine/           # Parse-safety scoring
  ai-rewriter/          # Rewrite suggestions
  jobs-feed/            # Job ingestion and seed
packages/
  scoring/              # Single source of truth for score formula
docs/                   # Product, security, deployment, ADR docs
infra/                  # Seed artifacts and infra config
```

## Quick start (local)

### 1) Prerequisites

- Node 20+
- pnpm
- Python 3.11+
- Docker Desktop

### 2) Install dependencies

```bash
pnpm install
```

### 3) Configure environment

Create env files from examples where applicable:

- `apps/web/.env.local`
- service-level `.env` files if required

### 4) Start stack

```bash
docker compose up --build
```

### 5) Start frontend

```bash
cd apps/web
pnpm dev
```

## API capabilities (student)

- Auth: register/login
- Profile: career profile create/update
- Resume: upload + parse
- ATS: parse-safety scoring
- JD: parse job descriptions
- Scorecard: student-to-JD scoring
- Recommendations: rewrite suggestions
- Jobs: browse seed/live feed
- Agent: deterministic student workflow run
- Export: resume PDF export jobs
- Assistant: FAQ/LLM student assistant

## Data model baseline

Alembic migration history is squashed to one clean student-only baseline:

- `services/core-api/migrations/versions/0001_student_baseline.py`

This baseline includes:

- auth/session (`users`, `session_tokens`)
- profile/resume (`career_profiles`, `resumes`, `resume_sections`, `resume_evidence`, `resume_export_jobs`, `ats_scans`)
- scoring (`job_descriptions`, `scorecards`, `recommendations`)
- jobs/orchestration (`jobs`, `agent_runs`)
- security/benchmark (`events_audit`, `benchmark_runs`)

## Validation commands

### Frontend typecheck

```bash
cd apps/web
pnpm exec tsc --noEmit
```

### Core API tests

```bash
cd services/core-api
python -m pytest -q
```

### Python AST sanity (touched services)

```bash
python -c "import ast, pathlib; [ast.parse(p.read_text(encoding='utf-8')) for p in pathlib.Path('services').rglob('*.py')]"
```

## Design rules (important)

- Keep feature folders only when they contain active code.
- No placeholder module directories.
- Keep API calls centralized in `apps/web/lib/api.ts`.
- Keep score formula centralized in `packages/scoring`.
- Do not reintroduce non-student product logic unless intentionally scoped and approved.

## Status

- Product direction: student-first, standalone.
- Migrations: clean student-only baseline.
- Module structure: flattened to real-code feature slices.
