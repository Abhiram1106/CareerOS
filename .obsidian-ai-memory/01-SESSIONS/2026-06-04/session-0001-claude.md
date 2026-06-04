---
date: 2026-06-04
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M6, M7, care-rag, quality-classifier, heatmap]
type: session
links: [active-goals, care-rag-architecture, error-memory]
---

# Session 2026-06-04 (2) — M6 + M7 Implementation

## What was done

### M6 — 7-Class Resume Quality Classifier (CARE-RAG Layer 2)

**`packages/scoring/careeros_scoring/formula.py`:**
- `classify_resume_quality()` — priority-ordered detection logic
- 7 classes evaluated in order (most severe wins):
  1. `ats_broken` — ats_parse_safety < 40 OR structural flags
  2. `structurally_weak` — profile_completeness < 40
  3. `interview_ready` — overall_score >= 70 (checked early to win)
  4. `role_misaligned` — ats >= 65 but jd_match < 35
  5. `high_potential_underwritten` — ats >= 65 but evidence < 40
  6. `keyword_weak` — jd_match < 40 AND skill_recall < 30
  7. `impact_weak` — default (content exists but no outcomes)
- `QUALITY_CLASS_LABELS` + `QUALITY_CLASS_GUIDANCE` dicts exported

**`__init__.py`:** exports all 3 new symbols

**`scorecard_dto.py`:** `QualityClassInfo` model + `quality_class` field on response

**`score_resume_handler.py`:** computes class after all scores, injects into response

**`api.ts`:** `QualityClassInfo` type + `quality_class?: QualityClassInfo` on `ScorecardResult`

**`usePlacementWorkspace.ts`:** `qualityClass` state + setter in `applyScorecard()`

**`match/page.tsx`:** `QualityClassBanner` component — icon + coloured badge + guidance text, shown between scan and readiness breakdown.

---

### M7 — JD Intelligence Heatmap (CARE-RAG Layer 5 UI)

**`vendor_simulation.py`:** `keyword_gap_analysis` now computes `frequency` (times each keyword appears in JD) for both matched and missing keywords.

**`scorecard_dto.py`:** `KeywordItem` + `MissingKeyword` gain `frequency: int = 1`

**`api.ts`:** `frequency?: number` on both keyword types

**`match/page.tsx`:** Keyword gap rebuilt as full heatmap:
- Match rate progress bar (colour = green/amber/red by % covered)
- Missing keywords: chip size scales with JD frequency (×N badge), colour = importance
- Present keywords: frequency badge on high-freq keywords
- Legend explaining chip size = JD frequency, colour = priority

---

## Verified
- `quality_class = "impact_weak"` correct for thin test resume
- Keyword frequency live in API response (e.g. `software ×1`, `python ×1`)
- `tsc --noEmit`: no errors
- All Python files: AST clean

---

## Next: M8 — Guided AI Resume Wizard

5-step wizard: Diagnose → Compare → Recommend → Rewrite → Verify
At `/resume/wizard` — rule-based, no LLM needed for MVP.
Uses `quality_class` from M6 as the entry point for Step 1 (Diagnose).

*Related: [[active-goals]] · [[care-rag-architecture]]*
