# AGENTS.md — CareerOS Campus AI

> Single source of truth for all AI tool adapters: Claude Code, Cursor, Copilot, Omnix.
> Read this file at session start before doing anything else.
> **Bootcamp context:** `.obsidian-ai-memory/02-PROJECTS/bootcamp-brief.md`

---

## What this project is

**CareerOS Campus AI** — Intel AI Bootcamp submission.
An Intel-optimized placement-readiness operating layer for Indian colleges.

- **Not** a job board, recruiter platform, LinkedIn scraper, or billing product.
- **Is** the system a TPO uses before campus drives: parse resumes → score vs JD → officer cohort dashboard → Intel benchmarks.
- **Scoring:** `packages/scoring/` is the only home of PlacementReadinessScore. Never duplicate it.
- **Intel:** OpenVINO for embedding inference, sklearnex for TF-IDF + KMeans. Real measured benchmarks only.

---

## Startup protocol (execute before every response)

1. Confirm repo markers: `AGENTS.md` + `.obsidian-ai-memory/` + `pnpm-workspace.yaml` + `services/core-api/`
2. Read memory in priority order (see Memory loop below).
3. Route to the correct workflow (see Routing table).
4. Emit the startup block, then begin work.

**Startup block:**
```
[CareerOS] Stack: Next.js 14 + FastAPI + Postgres/Redis | Mode: {mode}
Loaded: {files} | Known errors: {N} | Last session: {date}
Week {N} goal: {one-line from active-goals.md}
Routing: {workflow} | Agents: {roles}
```

---

## Memory loop

**Before work** — retrieve in order, stop at ~1 500-token budget:

| # | File | Load when |
|---|---|---|
| 1 | `.obsidian-ai-memory/02-PROJECTS/bootcamp-brief.md` | always — bootcamp context |
| 2 | `.obsidian-ai-memory/02-PROJECTS/project-context.md` | always |
| 3 | `.obsidian-ai-memory/02-PROJECTS/active-goals.md` | always |
| 4 | `.obsidian-ai-memory/02-PROJECTS/vault-index.md` | always |
| 5 | `.obsidian-ai-memory/03-ERRORS/error-memory.md` | always |
| 6 | `.obsidian-ai-memory/03-ERRORS/anti-patterns.md` | always |
| 7 | `.obsidian-ai-memory/04-DECISIONS/decisions.md` | architecture / design tasks |
| 8 | `.obsidian-ai-memory/05-ARCHITECTURE/README.md` | architecture tasks |
| 9 | `.obsidian-ai-memory/01-SESSIONS/` last 3 | context continuity |

**After work — memory write is not optional:**

| Condition | File | How |
|---|---|---|
| Meaningful files changed | `01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md` | Create from template |
| Bug fixed | `03-ERRORS/error-memory.md` | Append only |
| Non-trivial decision | `04-DECISIONS/decisions.md` | Append only |
| Project state changed | `02-PROJECTS/current-state.md` | Overwrite (snapshot) |
| Goal completed | `02-PROJECTS/active-goals.md` | Mark `[ ]` → `[x]` |

**Always commit the vault after writing:**
```bash
git add .obsidian-ai-memory/
git commit -m "memory: YYYY-MM-DD session digest"
```

---

## Engineering rules

**Universal:**
- Read vault before any response or edit. No exceptions.
- Never repeat known errors — check `error-memory.md` first.
- No secrets in any file, ever.
- Confirm before: `rm`, `DROP TABLE`, force push, `git reset --hard`, Alembic on non-empty DB.
- Verify before "done": `tsc --noEmit` clean + Python AST-parse clean. State result.
- One concern per commit. No WIP commits on `main`.
- Update docs when behaviour changes.

**Python (`services/`, `packages/scoring/`):**
- SQLAlchemy 2.0 mapped-column: `Mapped[T]` / `mapped_column(...)` — never `Column()`.
- Pydantic v2: `.model_dump()` not `.dict()`. `.model_validate()` not `.parse_obj()`.
- FastAPI route handlers stay slim — business logic in `services/<svc>/app/services/`.
- All cross-service HTTP via `services/core-api/app/services/clients.py` (httpx, never requests).
- Schema change → Alembic migration file. Never `entities.py` alone.
- Celery tasks: always close DB session in `finally`.

**TypeScript (`apps/web/`):**
- `strict: true`. No `any`. Unknown → `unknown`, then narrow.
- `"use client"` only for hooks, browser APIs, event handlers. Default: server component.
- All HTTP via `apps/web/lib/api.ts`. Never `fetch()` inline in components.
- No Tailwind, no CSS-in-JS — CSS variables in `apps/web/app/globals.css`.
- UI primitives: `CardSection`, `FormField`, `MetricTile` from `apps/web/components/ui/primitives.tsx`.

**Intel / Scoring:**
- `sklearnex.patch_sklearn()` must be called before any sklearn import, never after.
- OpenVINO: measure accuracy delta. If > 1% → stay at FP16, say so honestly.
- Benchmark numbers are real measurements. Never vendor headline claims.
- Score formula exclusively in `packages/scoring/`. Import it, never inline it.

---

## Routing table

| Signal | Workflow | Roles |
|---|---|---|
| resume-parser / pdfplumber / section extractor | feature-build + database | backend + architect + reviewer |
| match-engine / TF-IDF / embeddings / sklearnex | feature-build + intel | backend + data-science + reviewer |
| officer dashboard / batch / readiness heatmap | feature-build + frontend | frontend + backend + reviewer |
| intel-bench / OpenVINO / benchmark / latency | perf + intel | data-science + devops + reviewer |
| placement readiness score / scoring formula | feature-build | backend + data-science |
| proof-linked rewrite / AI rewriter / guardrails | feature-build | backend + security + reviewer |
| alembic / migration / schema / new table | feature-build + database | database + backend |
| JWT / role / RBAC / auth gate | feature-build + security | security + backend |
| ATS parse safety / heuristics / penalty | feature-build | backend + reviewer |
| pane / component / UI / animation | feature-build + frontend | frontend + reviewer |
| tsc error / type error | bug-fix | frontend + reviewer |
| error / broken / crash / exception | debug → bug-fix | debugger + security |
| slow / performance / optimize | debug + perf | data-science + devops |
| review / audit / quality | code-review | reviewer + security |
| refactor / clean / simplify | refactor | architect + reviewer |
| docker / compose / deploy | deployment | devops |
| docs / ADR / README | docs-update | docs |

---

## Stack map

| Layer | Tech | Path |
|---|---|---|
| Web app | Next.js 14, TypeScript strict, Motion animations | `apps/web/` |
| API client | Typed — never `fetch()` inline | `apps/web/lib/api.ts` |
| State hook | `useCareerOSWorkspace` | `apps/web/hooks/useCareerOSWorkspace.ts` |
| UI primitives | `CardSection`, `FormField`, `MetricTile`, `TiltCard` | `apps/web/components/ui/` |
| Core API | FastAPI 0.115, SQLAlchemy 2.0, Pydantic v2, Celery | `services/core-api/` |
| Auth | JWT + SessionTokens table + role claim | `services/core-api/app/services/auth.py` |
| DB models | SQLAlchemy 2.0 mapped-column | `services/core-api/app/models/entities.py` |
| Migrations | Alembic only — `AUTO_CREATE_TABLES=false` in prod | `services/core-api/migrations/versions/` |
| ATS engine | Rule-based parse-safety scorer | `services/ats-engine/app/main.py` |
| AI rewriter | Proof-linked JSON-schema rewriter | `services/ai-rewriter/app/main.py` |
| Resume parser | pdfplumber + python-docx + section extractor | `services/resume-parser/app/main.py` |
| Match engine | TF-IDF + embeddings + sklearnex (Week 2) | `services/match-engine/` — pending |
| Intel bench | OpenVINO + sklearnex harness (Week 5) | `services/intel-bench/` — pending |
| Scoring pkg | PlacementReadinessScore formula | `packages/scoring/` — pending |
| Contracts | JSON Schema (Resume, JD, Scorecard, Rewrite) | `packages/contracts/` |

---

## Safety gates

Stop and confirm before any of:
- Deleting files or directories
- Dropping or truncating database tables
- Running Alembic on a non-empty database
- Force-pushing any branch
- `git reset --hard`
- Writing real values to `.env` or `.env.example`
- Publishing to PyPI or npm
