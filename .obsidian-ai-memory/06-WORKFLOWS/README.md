---
tags: [workflows, procedures, dev]
type: workflow
updated: 2026-05-21
links: [_INDEX, api-index, errors-index]
---

# Workflows — CareerOS Campus AI

← [[_INDEX]] · [[api-index]] · [[errors-index]]

> Repeatable step-by-step procedures for common development tasks.
> AI tools read this for task-type routing. Humans read this for onboarding.

---

## Adding a new FastAPI endpoint

**If the domain is already migrated** (see [[05-ARCHITECTURE/layered-modules]] phase table):

1. DTO → `app/modules/<domain>/dto/`
2. Handler or query service → `mutation/` or `query/`
3. Repo/view → `app/adapter/db/persistence/<domain>/`
4. Controller → `app/api/controllers/<domain>_controller.py`; register in `api/router.py`
5. Remove any duplicate route from `main.py`

**If the domain is still legacy** (profile, resume, ats, dashboard as of 2026-05-21):

1. Add Pydantic schema to `services/core-api/app/schemas/contracts.py`
2. Add route handler to `services/core-api/app/main.py` (slim — validate + delegate only)
3. Add business logic to `services/core-api/app/services/<domain>.py`

**Always:**

4. If new table needed: Alembic migration in `migrations/versions/`
5. Typed wrapper in `apps/web/lib/api.ts`
6. UI in `apps/web/components/panes/` or `apps/web/modules/<domain>/` when modular
7. Verify: `tsc --noEmit` + Python AST parse
8. Update `05-ARCHITECTURE/layered-modules.md` when a domain migration completes

---

## Adding a new database table

1. Add model to `services/core-api/app/models/entities.py` (SQLAlchemy 2.0 mapped-column style)
2. Write migration: `cd services/core-api && alembic revision --autogenerate -m "add <table>"`
3. Review the generated migration file — autogenerate is approximate, always verify
4. Test: `alembic upgrade head` on clean DB + `alembic downgrade base` + `alembic upgrade head` again
5. Update `05-ARCHITECTURE/README.md` schema diagram

---

## Fixing a bug

1. Read `03-ERRORS/error-memory.md` — check if this bug was seen before
2. Read `03-ERRORS/anti-patterns.md` — check for relevant prevention rules
3. Reproduce with the smallest possible input
4. Fix
5. Add regression test
6. Verify: `tsc --noEmit` + Python AST parse
7. Append to `03-ERRORS/error-memory.md` using `templates/error-entry.md`
8. Write session digest

---

## Adding a new Python service

1. Create `services/<name>/app/main.py` (FastAPI, expose `/health`)
2. Create `services/<name>/requirements.txt`
3. Create `services/<name>/Dockerfile` (copy pattern from `services/ats-engine/Dockerfile`)
4. Add service to `docker-compose.yml` at repo root
5. Add httpx client function to `services/core-api/app/services/clients.py`
6. Wire the URL env var to `services/core-api/app/config.py` and `.env.example`
7. Update `05-ARCHITECTURE/README.md` system diagram
8. Update `02-PROJECTS/current-state.md`

---

## Running the Intel benchmark

```bash
# Week 5 — from repo root
python services/intel-bench/run.py --workload all --size medium
# Outputs: services/intel-bench/results/benchmark_runs.json
# Consumed by: apps/web/app/lab/intel/ (reads via GET /lab/benchmarks)
```

Rules:
- Run on actual Intel hardware (not cloud VM with unknown CPU)
- Run at three sizes: small (500 resumes), medium (5 000), large (20 000)
- Report p50, p95, throughput, accuracy delta, memory footprint
- If accuracy delta > 1% → stay at FP16, document the delta honestly

---

## Writing a session digest (end of session)

1. Create file: `.obsidian-ai-memory/01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md`
2. Copy `templates/session-digest.md`
3. Fill every field (write "none" or "N/A" explicitly — never leave blank)
4. Update [[02-PROJECTS/vault-index]] "Most recent session" · link from [[session-index]]
5. Check [[02-PROJECTS/active-goals]] — mark any completed goals `[x]`
6. Run: `git add .obsidian-ai-memory/ && git commit -m "memory: YYYY-MM-DD session digest"`

---

_Add new workflows here whenever a repeatable task is identified._
_Last updated: 2026-05-19_

*Related: [[_INDEX]] · [[api-index]] · [[errors-index]] · [[05-ARCHITECTURE/layered-modules]] · [[intel-index]] · [[MEMORY-WRITE-PROTOCOL]]*
