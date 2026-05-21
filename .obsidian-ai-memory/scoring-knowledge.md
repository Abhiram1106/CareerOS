---
tags: [hub, scoring, formula, moc, placement-readiness]
type: moc
created: 2026-05-21
updated: 2026-05-21
links: [_INDEX, MASTER_PLAN, intel-index, api-index, 04-DECISIONS/decisions]
---

# 📊 Scoring Knowledge — PlacementReadinessScore MOC

> **Single source of truth:** `packages/scoring/` (Python package).  
> Never duplicate this formula in `services/core-api`, `services/match-engine`, or frontend code.

← [[_INDEX]] | [[MASTER_PLAN]] | [[intel-index]] | [[api-index]] →

**Decision:** [[04-DECISIONS/decisions]] — *Score formula source of truth: `packages/scoring/`*

---

## Full formula

```
PlacementReadinessScore =
  0.35 × JD_Match
  0.20 × ATS_Parse_Safety
  0.20 × Evidence_Quality
  0.10 × Profile_Completeness
  0.10 × Interview_Readiness
  0.05 × Placement_Hygiene
```

All weights sum to **1.0**. Final score ∈ [0, 100].

Also documented in: [[02-PROJECTS/project-context#PlacementReadinessScore formula]] · [[05-ARCHITECTURE/README]] · [[02-PROJECTS/bootcamp-brief#Scoring formula]]

---

## JD_Match sub-formula

```
JD_Match =
  0.35 × TFIDF_Cosine
  0.35 × Embedding_Cosine      ← OpenVINO-accelerated (Week 2)
  0.20 × Required_Skill_Recall
  0.10 × Eligibility_Rule_Score
```

| Sub-component | Producer | Intel |
|---------------|----------|-------|
| TFIDF_Cosine | `services/match-engine/` | sklearnex-patched TF-IDF — [[intel-index]] |
| Embedding_Cosine | `services/match-engine/` | OpenVINO IR model — [[intel-index]] |
| Required_Skill_Recall | JD parser + resume sections | — |
| Eligibility_Rule_Score | CGPA, branch, backlogs, grad year | Rule-based |

---

## Score buckets (UI labels)

| Range | Label | Meaning |
|-------|-------|---------|
| 0–49 | High Risk | Major gaps vs JD / ATS / evidence |
| 50–69 | Borderline | Fixable before drive |
| 70–84 | Ready | Meets bar with minor polish |
| 85–100 | Strong | Top of cohort |

Used in: `/workspace` JD Match Scan tab · officer heatmaps ([[MASTER_PLAN#Week 4]]) · demo Scene 4–5 ([[02-PROJECTS/bootcamp-brief#The 3-minute demo script]])

---

## Component reference

### JD_Match (35%)
- **What:** How well resume matches pasted company JD (lexical + semantic + skills + hard eligibility).
- **Code path (Week 2):** `services/match-engine/` → persisted in `scorecards.jd_match` (planned).
- **UI:** Primary bar in score breakdown — [[05-ARCHITECTURE/frontend-ux]]

### ATS_Parse_Safety (20%)
- **What:** Parse-safety penalty (columns, tables, fonts, section structure) — not the legacy 5-metric ATS composite.
- **Code path:** `services/ats-engine/` (narrowed Week 2) + `resume-parser` flags.
- **Legacy:** `POST /ats/scan` composite — being replaced per [[02-PROJECTS/active-goals]]

### Evidence_Quality (20%)
- **What:** Action verbs, metrics in bullets, proof density in resume JSON.
- **Code path:** `packages/scoring/` + resume_sections evidence graph.

### Profile_Completeness (10%)
- **What:** Filled fields in `career_profiles` + user record.
- **Code path:** Overlaps `GET /dashboard` `profile_completeness` metric.

### Interview_Readiness (10%)
- **What:** Projects, internships, role-relevant depth (heuristic / LLM-assisted Week 2+).

### Placement_Hygiene (5%)
- **What:** Contact info, length, section order, Indian fresher conventions.

---

## Data model (planned)

| Table | Role |
|-------|------|
| `job_descriptions` | JD text, `skills_json`, `eligibility_json` |
| `scorecards` | Six components + composite + `resume_id` + `jd_id` |
| `recommendations` | Post-rewrite lift tracking |

→ Schema context: [[architecture-index#Data model]]

---

## Implementation checklist (Week 2)

- [ ] `packages/scoring/` package with unit tests
- [ ] `services/match-engine/` returns sub-scores only
- [ ] core-api `POST /scorecards/score` imports package — no inline math
- [ ] UI six bars + bucket + missing skills — [[02-PROJECTS/active-goals]]

---

## Anti-patterns

- Duplicating weights in FastAPI handlers
- Hardcoding bucket thresholds in frontend only (share from package)
- Using vendor Intel speed claims without `benchmark_runs` — [[intel-index]]

---

*Related: [[_INDEX]] · [[MASTER_PLAN]] · [[intel-index]] · [[api-index]] · [[architecture-index]] · [[02-PROJECTS/bootcamp-brief]] · [[02-PROJECTS/project-context]] · [[04-DECISIONS/decisions]] · [[05-ARCHITECTURE/README]]*
