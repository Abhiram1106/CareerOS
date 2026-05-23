---
tags: [session, week-2, scoring, match-engine]
tool: cursor
date: 2026-05-21
---

# Session digest — Week 2 kickoff (Cursor)

## Goal

Start Week 2 from vault context: JD match pipeline, scoring package, match-engine, workspace UI.

## Done

- **`packages/scoring/careeros_scoring/`** — PlacementReadinessScore + JD_Match weights, ATS flag penalties, resume heuristics; 4 unit tests pass.
- **`services/match-engine/`** (port 8005) — `POST /jd/parse`, `POST /match`; sklearnex patch; skill taxonomy; dual TF-IDF (word + char_wb) for embedding proxy until OpenVINO embeddings (Week 5).
- **core-api** — `POST /jd/parse`, `POST /scorecards/score`; layered handlers; `MATCH_ENGINE_URL`; Docker build context = repo root (includes scoring pkg).
- **docker-compose** — `match-engine` service + env on core-api/worker.
- **apps/web** — `api.parseJd`, `api.scoreResume`; workspace `handleScan` wired; raw sub-scores on bars, `overall_score` for total; missing/matched skills.

## Verify

- `tsc --noEmit` (apps/web): clean
- Python AST (scoring, match-engine, jd/scorecard modules): clean
- `pytest packages/scoring/tests`: 4 passed

## Open

- Narrow `ats-engine` to parse-safety-only endpoint (legacy composite still used by `/ats/scan`).
- Sentence-transformer / OpenVINO embedding path (documented as Week 5 intel).
- Officer dashboard (Week 4).

## Key paths

| Piece | Path |
|-------|------|
| Formula | `packages/scoring/careeros_scoring/formula.py` |
| Match | `services/match-engine/app/matcher.py` |
| Score API | `services/core-api/app/modules/scorecard/mutation/score_resume_handler.py` |
| UI | `apps/web/app/(app)/workspace/page.tsx` |
