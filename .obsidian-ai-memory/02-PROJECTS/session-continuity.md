# Session continuity — CareerOS (rolling handoff)

> **Overwrite this file at the end of every Cursor chat.**
> Next chat reads this **before** other memory. Detail lives in `01-SESSIONS/`.

---

## Last chat

| Field | Value |
|-------|-------|
| Updated | 2026-05-23 (student-first pivot committed) |
| Tool | cursor |
| Session file | `01-SESSIONS/2026-05-23/session-student-first-cursor.md` |
| User ask (latest) | Commit everything (code + Obsidian vault) |

---

## Active thread (max 5 bullets)

- Student-first flow shipped: Jobs search → deterministic agent → export queue
- `services/jobs-feed` on :8006; core-api orchestrates parser/ATS/match/rewriter/scoring
- Officer UI gated off by default (`ENABLE_OFFICER_SURFACE=false`)
- sklearnex benchmark documented in `docs/benchmarks/match-engine-sklearnex.md`
- Next: Week 4 officer dashboard OR Week 5 intel-bench UI panel + pitch deck

---

## Codebase snapshot

| Area | State |
|------|--------|
| Student loop | Jobs tab + Builder wizard + `POST /agent/run` + golden-path test |
| Week 2–3 | Scoring, proof-linked rewrite, recommendations — integrated in agent |
| Week 4 | Officer routes exist but feature-flagged |
| Week 5 | Demo script + sklearnex bench done; `intel-bench` service + lab UI pending |

---

## Verification (last run)

| Check | Result |
|-------|--------|
| `tsc --noEmit` (apps/web) | passed |
| Python AST (touched services) | passed |
| `test_agent_run_golden_path.py` | passed |

---

## Next chat — do these first

1. Read `docs/pitch/demo-script.md` if rehearsing bootcamp demo
2. Set Adzuna keys for live jobs or rely on `infra/seed/jobs.seed.json`
3. `alembic upgrade head` in core-api if not using `AUTO_CREATE_TABLES`

---

## Open risks / do not redo

- Do not duplicate PlacementReadinessScore outside `packages/scoring/`
- Do not commit `.env` / `.env.local` with secrets
- Streamlit full rewrite rejected — keep FastAPI + Next.js architecture

---

## Recent session trail (newest first)

- `01-SESSIONS/2026-05-23/session-student-first-cursor.md` — student-first pivot + commits
- `01-SESSIONS/2026-05-23/session-1019-cursor.md` — Week 2 + audit hardening
