# Session continuity — CareerOS (rolling handoff)

> **Overwrite this file at the end of every Cursor chat.**
> Next chat reads this **before** other memory. Detail lives in `01-SESSIONS/`.

---

## Last chat

| Field | Value |
|-------|-------|
| Updated | 2026-05-21 (phases 4–7) |
| Tool | cursor |
| Session file | `01-SESSIONS/2026-05-21/session-phases-4-7-cursor.md` |
| User ask (latest) | Complete layered phases 4, 5, 6, 7 one by one; then Week 2 |

---

## Active thread (max 5 bullets)

- **Layered refactor complete:** Phases 1–7 done — core-api routes on controllers; `main.py` slim; satellites scaffolded
- **Frontend:** inline `fetch` removed from login/register/workspace; export download via `api.downloadExport`
- **ATS/dashboard:** null-safe profile via `profile_fields_for_scan` (fixes missing-profile crash on dashboard)
- **Next product work:** Week 2 per `active-goals.md` — JD parser, match-engine, `packages/scoring/`, score UI
- Memory workflow unchanged: digest + continuity + `memory:` commit when meaningful

---

## Codebase snapshot

| Area | State |
|------|--------|
| Layered refactor | **Phases 1–7 complete** |
| `core-api/main.py` | `/health` + startup only |
| `api/router.py` | auth, profile, resume, export, ats, dashboard |
| Week goal | Week 2: JD parser, match-engine, scoring pkg, score UI |

---

## Verification (last run)

| Check | Result |
|-------|--------|
| `tsc --noEmit` (apps/web) | passed (2026-05-21 phases 4–7) |
| Python AST (core-api + satellites) | passed (2026-05-21 phases 4–7) |

---

## Next chat — do these first

1. Read this file + `active-goals.md` Week 2 section
2. Start Week 2: `packages/scoring/`, match-engine, JD parser per bootcamp plan
3. Shutdown protocol from `.cursor/MEMORY-WORKFLOW.md` when session ends

---

## Open risks / do not redo

- Do not re-inline routes into `main.py`
- `GET /profile` / ATS scan use defaults when profile row missing — keep `profile_fields_for_scan`
- ai-rewriter resume text now uses real `\n` newlines (was escaped `\\n` in old main) — intentional fix
