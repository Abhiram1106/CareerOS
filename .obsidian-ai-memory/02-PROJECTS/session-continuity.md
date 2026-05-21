# Session continuity — CareerOS (rolling handoff)

> **Overwrite this file at the end of every Cursor chat.**
> Next chat reads this **before** other memory. Detail lives in `01-SESSIONS/`.

---

## Last chat

| Field | Value |
|-------|-------|
| Updated | 2026-05-21 19:00 IST |
| Tool | cursor |
| Session file | `01-SESSIONS/2026-05-21/session-1900-cursor.md` |
| User ask (latest) | Update `.cursor` docs: commit memory + session write-up after every chat for traceability |

---

## Active thread (max 5 bullets)

- Layered architecture: Phases 1–3 done (scaffold, auth, profile); Phase 4 resume+export next
- Vault synced: `05-ARCHITECTURE/layered-modules.md`, `current-state.md`, `vault-index.md`
- Cursor workflow: **`.cursor/MEMORY-WORKFLOW.md`** — shutdown = digest + continuity + `memory:` commit every chat
- API paths unchanged: `/profile`, `/auth/*` via `api/router.py`
- User wants **memory git commit after every Cursor chat** unless they say otherwise

---

## Codebase snapshot

| Area | State |
|------|--------|
| Layered refactor | Phase 3 profile **done**; Phase 4 resume+export **next** |
| Legacy `main.py` | `/resumes/*`, `/exports/*`, ATS, dashboard still inline |
| Week goal | Week 2: JD parser, match-engine, `packages/scoring/`, score UI |

---

## Verification (last run)

| Check | Result |
|-------|--------|
| `tsc --noEmit` (apps/web) | passed (2026-05-21 profile phase) |
| Python AST (core-api) | passed (2026-05-21 profile phase) |

---

## Next chat — do these first

1. Read this file + latest `01-SESSIONS/2026-05-21/session-*-cursor.md`
2. Phase 4: migrate resume + export off `main.py` (see `05-ARCHITECTURE/layered-modules.md`)
3. Run shutdown protocol from `.cursor/MEMORY-WORKFLOW.md` before ending chat

---

## Open risks / do not redo

- Do not remove `main.py` routes until each domain is on `api/router.py`
- Memory commit is **separate** from code commits (`memory:` prefix)
- `GET /profile` now safe when profile row missing (defaults) — do not revert to nullable deref

---

## Recent session trail (newest first)

| Date | File | Summary |
|------|------|---------|
| 2026-05-21 | `01-SESSIONS/2026-05-21/session-1900-cursor.md` | Cursor memory workflow + continuity file |
| 2026-05-21 | `01-SESSIONS/2026-05-21/session-1800-cursor.md` | Phase 3 profile layered migration |
| 2026-05-21 | `01-SESSIONS/2026-05-21/session-1700-cursor.md` | Vault sync + auth migration |
| 2026-05-20 | `01-SESSIONS/2026-05-20/session-1430-cursor.md` | Frontend shell / hero |
