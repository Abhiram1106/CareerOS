# Session Continuity — CareerOS Campus AI

> **Overwrite this file at the end of every Cursor chat** (see `.cursor/MEMORY-WORKFLOW.md`).
> Next chat: read this first, then `project-context.md` and `active-goals.md`.

**Last updated:** 2026-05-23 (Week 2 + audit hardening complete)

---

## Where we left off

- **Week 2 demo loop:** complete end-to-end — resume upload → JD parse → match-engine → `packages/scoring` → readiness UI with six bars + bucket badge.
- **Audit P0/P1 closed:**
  - RBAC (`require_student` / `require_officer`) on all role-specific routes.
  - Honest `semantic_method: "embedding_proxy_tfidf"` field + UI tooltip.
  - `ats_flags` and `college_id` (request → user fallback) persisted on scorecards.
  - Golden-path API test (`services/core-api/tests/test_scoring_golden_path.py`).
  - Hardened formula tests (`packages/scoring/tests/test_formula.py`).
- **Legacy cleanup:** deleted orphaned `components/panes/**`, `components/SectionNav.tsx`, `components/workspace/WorkspaceTabs.tsx`, `components/layout/{AppHeader,SiteNav,AppFooter}.tsx`, `hooks/useCareerOSWorkspace.ts`. Workspace screen is driven solely by `usePlacementWorkspace`.
- **Verification:** `tsc --noEmit` (apps/web) clean; Python AST parse clean across 107 files.

Latest digest: [[01-SESSIONS/2026-05-23/session-1019-cursor]]

---

## Week 3 — next product work

1. `services/ai-rewriter` retargeted: proof-linked JSON-schema output, `unsupported_claims[]`, system prompt from research §"Guardrails".
2. Before/after diff UI in `apps/web` (with evidence callouts on each rewritten bullet).
3. ATS-safe PDF export wired through existing WeasyPrint Celery task → `POST /resumes/{id}/export` in the layered structure.

Checklist: [[02-PROJECTS/active-goals]] · API plan: [[api-index]] · Formula: [[scoring-knowledge]] · Architecture: [[05-ARCHITECTURE/layered-modules]]

---

## Verification (last known — 2026-05-23)

| Check | Status |
|-------|--------|
| `tsc --noEmit` (apps/web) | **pass** |
| Python AST parse (core-api, ats-engine, match-engine, scoring, tests) | **pass** (107 files) |
| Golden-path API integration test | **green** |
| Formula unit tests | **green** |

---

## Open risks

- Some routes still in `services/core-api/app/main.py` — finish layered extraction during Week 3.
- `apps/web/modules/scorecard/services/scorecardService.ts` is a seed file with no caller yet — wire `usePlacementWorkspace` through it during Week 3 to avoid bit-rot.
- No CI runner; all verification is local.

---

## Do not repeat

- [[03-ERRORS/error-memory]] · [[03-ERRORS/anti-patterns]] · hub: [[errors-index]]
- Don't post tests to `/register` — auth router is mounted at `/auth` (`POST /auth/register`).
- Don't monkeypatch async clients with sync functions; wrap return values in `async def _async(v): return v`.
- Don't share an in-memory SQLite engine across tests — function-scope it with `StaticPool`.

---

*Related: [[_INDEX]] · [[session-index]] · [[MASTER_PLAN]] · [[02-PROJECTS/active-goals]] · [[02-PROJECTS/current-state]]*
