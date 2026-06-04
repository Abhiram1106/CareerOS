---
date: 2026-06-04
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M10, care-rag, skill-graph, gap-analysis]
type: session
links: [active-goals, care-rag-architecture, error-memory]
---

# Session 2026-06-04 (5) — M10: CARE-RAG Skill Graph Index

## What was done

### M10 — Skill Graph Index (CARE-RAG Layer 3D)

**`services/match-engine/app/skill_taxonomy.py`** — SKILL_GRAPH added:
- 80+ skills with directed adjacency `(neighbour, distance)` edges
- Ecosystems covered: Python, JS/TS, Java, DevOps/Cloud, Data/ML, CS concepts
- Asymmetric edges reflect learning direction
- Distance semantics: 1=direct prereq, 2=same family, 3=same domain
- `get_adjacent_skills(known, max_distance, exclude, limit)` — returns reachable neighbours sorted by distance
- `skill_gap_with_graph(known, missing)` — enriches each missing skill with `{distance, nearest_known, reachable}`
  Distinguishes "skill gap" (no path in graph) from "resume gap" (reachable but not mentioned)

**`services/match-engine/app/main.py`** — 2 new skill graph endpoints:
- `POST /skills/adjacent` — returns d1/d2/d3 neighbours of known skills
- `POST /skills/gap-with-graph` — enriches missing skills with graph context

**`services/core-api/app/services/clients.py`:**
- `skill_gap_with_graph()` and `get_adjacent_skills()` HTTP clients (fire-and-return, return empty on error)

**`scorecard_dto.py`:** `GraphGapItem` model + `graph_gap` field on `ScorecardScoreResponse`

**`score_resume_handler.py`:** calls `skill_gap_with_graph()` on every scorecard — missing required skills enriched with graph distance

**`api.ts`:** `GraphGapItem` type + `graph_gap?: GraphGapItem[]` on `ScorecardResult`

**`usePlacementWorkspace.ts`:** `graphGap` state + setter

**`match/page.tsx`:** Missing keyword chips now show `d1`/`d2` badge when a graph path exists from known skills. Tooltip shows "X hops from your [nearest_skill]". Legend updated.

---

## Verified results

```
Python + Docker (d≤1) adjacent → ci/cd, django, fastapi, kubernetes, linux, numpy, pandas
Gap enrichment (known: python, docker, git):
  fastapi   → d1 from python   (reachable: resume gap, not skill gap)
  kubernetes → d1 from docker  (reachable)
  sql        → d1 from python  (reachable)
  machine learning → d2 from python (reachable)
  react      → no path         (genuine skill gap)
Scorecard graph_gap: REST API → d1 from fastapi
```

tsc clean. AST clean.

---

## CARE-RAG milestone tracker

| M# | Milestone | Status |
|---|---|---|
| M6 | 7-class quality classifier | ✅ |
| M7 | JD intelligence heatmap | ✅ |
| M8 | Guided AI wizard | ✅ |
| M9 | Vector store + retrieval | ✅ |
| M10 | Skill graph index | ✅ |
| M11 | Feedback loop wiring | 🔴 Next |
| M12 | Evolution timeline UI | Pending |

---

## Next: M11 — Feedback Loop Wiring

Wire accepted suggestions + interview outcomes back into the knowledge base.
- When recommendation accepted → `POST /vector/user-signal` with `suggestion_accepted`
- When application → interview/offer → tag scorecard as positive outcome
- Surface to user: "X students who made this change got interviews"

*Related: [[active-goals]] · [[care-rag-architecture]]*
