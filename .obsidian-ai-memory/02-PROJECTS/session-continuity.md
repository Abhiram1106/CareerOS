# Session continuity — CareerOS (rolling handoff)

> **Overwrite this file at the end of every Cursor chat.**
> Next chat reads this **before** other memory. Detail lives in `01-SESSIONS/`.

---

## Last chat

| Field | Value |
|-------|-------|
| Updated | 2026-05-21 (workflow + commits) |
| Tool | cursor |
| Session file | `01-SESSIONS/2026-05-21/session-phases-4-7-cursor.md` + workflow follow-up in digest |
| User ask (latest) | Extend Cursor shutdown: **code commit + memory commit + push** each chat; perform now |

---

## Active thread (max 5 bullets)

- **Layered refactor:** Phases 1–7 complete — ready for Week 2 product work
- **Cursor shutdown:** code commit → `memory:` commit → `git push` (see `.cursor/MEMORY-WORKFLOW.md`)
- **This chat:** committed phases 4–7 code + vault; pushed if remote allowed
- **Unstaged (if any):** unrelated `apps/web` layout/marketing tweaks — commit separately when ready
- **Next:** Week 2 — JD parser, match-engine, `packages/scoring/`, score UI

---

## Codebase snapshot

| Area | State |
|------|--------|
| Layered refactor | Phases 1–7 complete |
| `core-api/main.py` | health + startup only |
| Git workflow | dual commits + push per meaningful Cursor chat |

---

## Verification (last run)

| Check | Result |
|-------|--------|
| `tsc --noEmit` (apps/web) | passed (phases 4–7) |
| Python AST | passed (core-api + satellites) |

---

## Next chat — do these first

1. Read this file + `active-goals.md` Week 2
2. Start Week 2 work user picks (JD parser / match-engine / scoring)
3. Shutdown: code commit + memory commit + push (unless user says no)

---

## Open risks / do not redo

- Never bundle code into `memory:` commits
- Never skip push without user saying so (default: push after commits)
