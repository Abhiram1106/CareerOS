# AI_RULES.md — CareerOS Campus AI

Universal engineering rules for every AI tool on this project.
All adapters (Claude Code, Cursor, Copilot) must follow these in addition to
their tool-specific config. See `AGENTS.md` for routing and `STARTUP_PROTOCOL.md`
for session execution order.

---

## Non-negotiable rules

| Rule | Detail |
|---|---|
| **Memory first** | Read `.obsidian-ai-memory/` before every response or edit. |
| **No repeated errors** | Check `03-ERRORS/error-memory.md` before diagnosing. |
| **No secrets** | Never commit or log JWT secrets, DB passwords, API keys, or private keys. |
| **Verify before done** | `tsc --noEmit` clean (apps/web) + Python AST-parses clean (services/*). State result. |
| **No fabrication** | `services/ai-rewriter` must never invent facts. Flag unsupported claims — never silently include them. |
| **Small changes** | One concern per commit. No WIP commits on `main`. |
| **Confirm destructive ops** | `rm`, `DROP TABLE`, force push, `git reset --hard`, Alembic on live DB — stop and ask. |
| **Update docs** | Changed endpoint or behaviour without updated README/ADR is incomplete. |
| **Write session digest** | After every session > 15 min or with meaningful changes. |
| **Score formula in one place** | `packages/scoring/` is the canonical implementation. Never duplicate it in service code. |

---

## Python rules (`services/`, `packages/scoring/`)

- **FastAPI route handlers stay slim.** Business logic lives in `services/<svc>/app/services/`, not in route functions. Route = validate input, call service, return response.
- **SQLAlchemy 2.0 mapped-column style.** Use `Mapped[T]` / `mapped_column(...)`. No legacy `Column()`.
- **Pydantic v2.** `BaseModel` + `Field(...)`. Email fields use `EmailStr`. No `.dict()` — use `.model_dump()`.
- **Type-hint all public functions.** Use `from __future__ import annotations` if forward refs are needed.
- **Alembic migrations are real files.** `AUTO_CREATE_TABLES=false` once Week 1 migration lands. Never add tables by modifying `entities.py` alone — write a migration.
- **Celery tasks always close the DB session in `finally`.** See `services/core-api/app/workers/tasks.py` for the pattern.
- **httpx for all cross-service calls.** Never use `requests`. All cross-service clients live in `services/core-api/app/services/clients.py`.
- **Config via `os.getenv()` with a safe fallback.** Validated at startup. Missing required config → fail fast.
- **`__pycache__/` and `*.pyc` are never committed.** `.gitignore` covers them.

---

## TypeScript / Next.js rules (`apps/web/`)

- **`strict: true`.** No `any`. Unknown types use `unknown` and are narrowed.
- **React function components only.** No class components.
- **"use client" only when required.** Default to server components. Add `"use client"` only for hooks, browser APIs, or event handlers.
- **All HTTP goes through `lib/api.ts`.** Never `fetch()` inline from components.
- **State: `useState` + `useMemo` + `useCareerOSWorkspace` hook.** No global state library (Redux/Zustand/Jotai) unless a concrete need is documented in an ADR.
- **UI primitives first.** Use `CardSection`, `FormField`, `MetricTile` from `apps/web/components/ui/primitives.tsx` before writing new layout.
- **Pane components in `apps/web/components/panes/`.** Section cards in `apps/web/components/panes/sections/`.
- **CSS variables in `globals.css`.** Extend the dark-theme tokens, don't replace them. No Tailwind, no CSS-in-JS until an ADR approves it.
- **Inline styles** (`style={{...}}`) are tolerated for one-off tweaks on existing components. New reusable components use CSS classes.
- **Buttons need `type` attribute.** `type="button"` for non-submit; `type="submit"` inside forms.
- **Form fields use `FormField` with a real `label`.** No unlabelled inputs.

---

## Scoring / Intel rules (`packages/scoring/`, `services/match-engine/`, `services/intel-bench/`)

- **Formula weights are fixed until an ADR changes them.** `PlacementReadinessScore = 0.35×JD_Match + 0.20×ATS_Parse_Safety + 0.20×Evidence_Quality + 0.10×Profile_Completeness + 0.10×Interview_Readiness + 0.05×Placement_Hygiene`.
- **JD_Match sub-formula:** `0.35×TFIDF_Cosine + 0.35×Embedding_Cosine + 0.20×Required_Skill_Recall + 0.10×Eligibility_Rule_Score`.
- **Intel benchmarks use real measured numbers only.** No mocked latency. Run at three dataset sizes (500 / 5 000 / 20 000 resumes). Report p50, p95, throughput, accuracy delta, memory footprint.
- **OpenVINO conversion:** measure accuracy delta before shipping INT8. Fall back to FP16 if delta > 1% on match quality.
- **sklearnex:** patch with `sklearnex.patch_sklearn()` before importing scikit-learn estimators. Never patch after estimator instantiation.

---

## Import order

Python: `stdlib → third-party → first-party`, separated by blank lines.
TypeScript: `external packages → workspace packages → relative imports`.
No barrel files (`index.ts` re-exports) unless they remove real import ceremony.

---

## File layout rules

- Tests live next to the code they test: `services/<svc>/tests/`, `apps/web/__tests__/`.
- Cross-domain end-to-end tests live in `tests/` only.
- Per-service docs live in `services/<svc>/README.md`.
- Top-level project docs live in `docs/`.
- Per-package docs live in `packages/<pkg>/README.md`.
