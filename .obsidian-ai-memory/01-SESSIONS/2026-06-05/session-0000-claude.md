---
date: 2026-06-05
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M11, M12, care-rag, feedback-loop, evolution-timeline]
type: session
links: [active-goals, care-rag-architecture, error-memory]
---

# Session 2026-06-05 — M11 + M12: Feedback Loop + Evolution Timeline

## M11 — CARE-RAG Feedback Loop Wiring

**`recommendation_repo.py`:**
- `set_feedback(rec_id, accepted)` — sets `recommendations.accepted` bool
- `find_by_id_for_user()` for safe lookup

**`recommendation_controller.py`:**
- `PUT /recommendations/feedback/{rec_id}` `{accepted: bool}`
- Sets DB flag + fires `vector_user_signal()` to ChromaDB user_memory
- signal_type: `suggestion_accepted` | `suggestion_rejected`

**`sections_controller.py` (update_application)**:
- Made async to fire vector signals
- When status → `interview` or `offer`: logs `outcome_interview`/`outcome_offer`
  to user_memory collection + records in `events_audit` table
- Finds latest scorecard for user to tag as positive outcome

**`api.ts`:** `api.recordRecommendationFeedback(token, recId, accepted)` wrapper

**`RewriteDiffPanel.tsx`:**
- `FeedbackButtons` component: Apply ✓ / Skip ✗ per rewrite card
- Fire-and-forget `handleFeedback()` — failure never blocks UX
- Visual state: idle → accepted (green) / rejected (grey)

**Verified:** feedback ok, suggestion_accepted signal, interview outcome signal, `user_memory=2` in ChromaDB after both.

---

## M12 — Resume Evolution Timeline

**`dashboard_controller.py`:**
- `score-history` now returns `version` (1-indexed) and `quality_class` per scan
- `classify_resume_quality()` called for each historical scorecard
- Query extended to include `ats_safety`, `evidence_quality`, `profile_completeness`, `jd_match`

**`api.ts`:** score-history type updated with `version`, `quality_class`

**`dashboard/page.tsx`:**
- `EvolutionTimeline` component: horizontal stepper, each scan shown as QC icon + score + version
- Colour-coded per quality_class
- Connector lines between versions
- "🏆 Interview Ready" callout when latest scan reaches that class
- Shown below sparkline in Readiness Snapshot card

**Verified:** 15 history entries with version + quality_class in API. tsc + AST clean.

---

## CARE-RAG Complete: All 7 milestones done

| M# | Milestone | Status |
|---|---|---|
| M6 | 7-class quality classifier | ✅ |
| M7 | JD intelligence heatmap | ✅ |
| M8 | Guided AI wizard | ✅ |
| M9 | Vector store + retrieval | ✅ |
| M10 | Skill graph index | ✅ |
| M11 | Feedback loop wiring | ✅ |
| M12 | Evolution timeline UI | ✅ |

## Remaining post-MVP
B2B officer portal, LinkedIn OAuth, OpenVINO IR, learning-to-rank model.

*Related: [[active-goals]] · [[care-rag-architecture]]*
