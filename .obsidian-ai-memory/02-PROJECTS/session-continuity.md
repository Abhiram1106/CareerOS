# Session Continuity — CareerOS Campus AI

> **Overwrite this file at the end of every Cursor chat** (see `.cursor/MEMORY-WORKFLOW.md`).
> Next chat: read this first, then `project-context.md` and `active-goals.md`.

**Last updated:** 2026-05-21 (Obsidian graph system complete)

---

## Where we left off

- **Obsidian graph system:** **DONE** — all 5 hub MOCs + Step 6 wikilinks on project, errors, decisions, architecture, workflows, lessons, and 12 session notes.
- **Hubs:** [[_INDEX]], [[MASTER_PLAN]], [[architecture-index]], [[session-index]], [[api-index]], [[scoring-knowledge]], [[intel-index]], [[errors-index]]
- **Layered architecture:** Phases 1–7 complete (`main.py` = health only).
- **Git:** `main` @ layered refactor + memory workflow docs; latest vault commit pending user push after graph commit.

---

## Week 2 — next product work (not vault)

1. JD parser → `job_descriptions` + `/jd/parse`
2. `services/match-engine/` — TF-IDF + embeddings + sklearnex ([[intel-index]])
3. `packages/scoring/` — [[scoring-knowledge]] formula only
4. Score breakdown UI wired to real API

Checklist: [[02-PROJECTS/active-goals]] · API plan: [[api-index]] · Formula: [[scoring-knowledge]]

---

## Verification (last known)

| Check | Status |
|-------|--------|
| `tsc --noEmit` (apps/web) | pass (phases 4–7 session) |
| Python AST (core-api + satellites) | pass |

---

## Open risks

- `current-state.md` body still describes pre–Phase 4 snapshot; graph pass added note at top — refresh snapshot when convenient.
- Week 2 services (`match-engine`, `packages/scoring/`) not started.

---

## Do not repeat

- [[03-ERRORS/error-memory]] · [[03-ERRORS/anti-patterns]] · hub: [[errors-index]]

---

*Related: [[_INDEX]] · [[session-index]] · [[MASTER_PLAN]] · [[02-PROJECTS/active-goals]]*
