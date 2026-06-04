---
tags: [architecture, care-rag, rag, ai, pipeline]
type: reference
updated: 2026-06-04
links: [active-goals, scoring-knowledge, architecture-index]
---

# CARE-RAG Architecture — CareerOS Intelligence Pipeline

← [[active-goals]] · [[architecture-index]]

> **CARE-RAG** = Continuous Adaptive Resume Enhancement using Retrieval-Augmented Generation.
> This document maps each CARE-RAG layer to the current codebase and the planned build.

---

## The 7-Layer Pipeline

```
Resume + JD Upload
        ↓
[Layer 1] Ingestion & Structured Extraction
        ↓
[Layer 2] Resume Quality Classification (7 classes)
        ↓
[Layer 3] Multi-Index Knowledge Base (vector store)
        ↓
[Layer 4] Hybrid Retrieval (semantic + BM25 + skill graph + outcome)
        ↓
[Layer 5] RAG Reasoning: Diagnose → Compare → Recommend → Rewrite → Verify
        ↓
[Layer 6] Feedback Learning Loop (accepted suggestions → outcome signals)
        ↓
[Layer 7] Evaluation + Guardrail (confidence, provenance, truthfulness)
        ↓
Job Search / Smart Matching → Outcome Tracking → Knowledge Base Improvement
```

---

## Layer 1 — Ingestion & Extraction

### Status: ✅ Built

| Component | Location | Notes |
|---|---|---|
| PDF/DOCX parser | `services/resume-parser/` | pdfplumber + python-docx + OCR fallback |
| Section extractor | `app/extractor.py` | heading heuristics + alias map |
| JD parser | `services/match-engine/app/jd_parser.py` | skills + eligibility extraction |
| Structured profile | `services/core-api/app/models/entities.py` | WorkExperience, Education, Skill, Project, Cert |
| User social links | `users.linkedin_url`, `github_url`, `phone`, `portfolio_url` | Added migration 0003 |

### Planned additions
- LinkedIn OAuth → auto-populate structured sections (Post-MVP)
- Portfolio/GitHub crawl → extract project evidence (Post-MVP)

---

## Layer 2 — Resume Quality Classification

### Status: ⚠️ Partial (4 buckets → upgrading to 7 classes)

**Current:** `high-risk / borderline / ready / strong` (score-based)

**Target — 7 diagnostic classes:**

| Class | Detection Logic | Action Prompt |
|---|---|---|
| ATS Broken | ats_parse_safety < 40 OR table_detected + two_column flags | "Fix formatting — ATS cannot read your resume" |
| Structurally Weak | profile_completeness < 40 OR missing_standard_headings | "Add missing sections: Education, Skills, Projects" |
| Keyword Weak | jd_match < 40 AND skill_recall < 30 | "Your skills exist but aren't in your resume" |
| Impact Weak | evidence_quality < 40 (no metrics, no strong verbs) | "Quantify your bullets — add numbers and outcomes" |
| Role Misaligned | jd_match < 35 despite ats_parse_safety > 65 | "Good resume, wrong role — tailor it to this JD" |
| High Potential, Underwritten | ats_parse_safety >= 65 AND evidence_quality < 40 | "You have the skills — your resume doesn't show it" |
| Interview Ready | overall_score >= 70 | "Strong profile — focus on JD-specific tailoring" |

**Implementation:** `packages/scoring/careeros_scoring/formula.py` → `classify_resume_quality()`
Deterministic from existing scores — no new infra.

---

## Layer 3 — Multi-Index Knowledge Base

### Status: ❌ Not built (M9 milestone)

**5 indexes planned:**

### A. Resume Pattern Index
- Anonymised resume chunks from all scored resumes (quality_class = Interview Ready)
- Grouped by role family (frontend, backend, data, devops, etc.)
- Enables: "Resumes like yours that got interviews had X"

### B. JD Intelligence Index
- All parsed JDs grouped by role, industry, experience level
- Keyword frequencies, must-have vs nice-to-have skill weights
- Enables: JD heatmap, trending skills by role

### C. Outcome Index
- Resume version → application status → interview/offer signal
- Positive: interview_received, offer_received
- Negative: rejected after X days, no response
- Enables: outcome-weighted retrieval

### D. Skill Graph Index
```
React → JavaScript → Frontend → REST API → UI Components
Python → Pandas → SQL → Dashboard → Data Analyst
Java → Spring Boot → REST API → Backend Developer
Docker → Kubernetes → DevOps → CI/CD → Cloud
```
- Stored in `skill_taxonomy.py` as adjacency dict
- Enables: "You know Python — also add Pandas and SQL"

### E. User Career Memory Index
- Per-user: all resume versions, target roles, skill growth, accepted/rejected suggestions
- Enables: personalised recommendations that remember what the user has tried before

**Tech choice:** ChromaDB (embedded, no external API, runs in match-engine container)

---

## Layer 4 — Hybrid Retrieval

### Status: ❌ Not built (part of M9)

| Retrieval Type | Purpose | Implementation |
|---|---|---|
| Semantic (vector) | Find resumes/JDs with similar meaning | MiniLM embeddings already built |
| Keyword / BM25 | Find exact JD keyword matches | TF-IDF already in match-engine |
| Skill graph | Find related skills and missing families | Skill graph (M10) |
| Outcome-based | Find resumes that led to interviews for similar JDs | Outcome Index (M9) |
| User history | Find user's older resume versions, ignored strengths | User Memory Index (M9) |

---

## Layer 5 — RAG Reasoning Engine

### Status: ⚠️ Partial (rule-based only, no retrieval)

**Current:** Proof-linked rewriter does STAR verb upgrade + filler removal deterministically.
**Target:** Diagnose → Compare → Recommend → Rewrite → Verify with retrieved context.

**5-step flow:**

```
Diagnose:   quality_class + top 3 score gaps identified
Compare:    retrieve top-5 similar successful resumes from Pattern Index
Recommend:  prioritised fixes with estimated Δscore per fix
Rewrite:    generate improved bullets using retrieved patterns as grounding
Verify:     re-score and surface before/after delta; check for fabrication
```

**Provenance example:**
> "Suggested because this JD mentions REST APIs 4 times and 78% of Interview Ready
> backend resumes in our knowledge base include API integration evidence."

---

## Layer 6 — Feedback Learning Loop

### Status: ⚠️ Partial (outcome tracking exists, not wired to retrieval)

**What exists:**
- `recommendations.accepted` field (bool)
- `job_applications.status` (saved/applied/screening/interview/offer/rejected)
- `events_audit` table (all actions logged)

**What's missing (M11):**
- When suggestion accepted → log `care_rag.suggestion.accepted` to EventAudit
- When application → interview/offer → tag source scorecard as positive outcome
- Use positive-outcome scorecards to populate Resume Pattern Index preferentially
- Weight retrieved examples by outcome success rate

**Learning signals:**
| Signal | Meaning | Effect |
|---|---|---|
| Suggestion accepted | Recommendation was useful | Boost similar retrievals |
| Suggestion rejected | Recommendation irrelevant | Demote similar retrievals |
| Score improved after edit | Optimization worked | Confirm pattern |
| Application → interview | Resume pattern successful | Add to Outcome Index |
| Application → offer | Strong match signal | Highest-weight outcome |
| No response | JD match still weak | Flag pattern for review |

---

## Layer 7 — Evaluation & Guardrail

### Status: ✅ Partially built

| Guardrail | Status | Location |
|---|---|---|
| Confidence score on each suggestion | ✅ Built | `recommendations.confidence` |
| Unsupported claim detection | ✅ Built | `proof_linked_rewrite_handler.py` |
| Anti-fabrication gate | ✅ Built | `unsupported_claims[]` in response |
| Evidence source citation | ❌ Missing | Planned for M9 (provenance) |
| Before/after score delta | ✅ Built | Score history + sparkline |
| Truthfulness warning display | ⚠️ Partial | Shown in rewrite panel, not in wizard |

**Target for every suggestion:**
```json
{
  "suggestion": "Add REST API integration evidence to your Projects section",
  "confidence": 0.84,
  "evidence_source": "12 Interview Ready backend resumes in knowledge base",
  "estimated_score_lift": "+8 points on JD Match",
  "truthfulness_note": "Only add if your project actually used APIs"
}
```

---

## Implementation Priority Map

| Milestone | Layer | Infra needed | Effort |
|---|---|---|---|
| M6 — 7-class classifier | 2 | None (uses existing scores) | Small |
| M7 — JD heatmap UI | 5 | None (data already returned) | Small |
| M8 — Guided wizard | 5 | None (rule-based) | Medium |
| M9 — Vector store | 3+4 | ChromaDB service | Large |
| M10 — Skill graph | 3D | Extend skill_taxonomy.py | Medium |
| M11 — Feedback loop | 6 | EventAudit wiring | Medium |
| M12 — Evolution timeline | 7 | Score history already exists | Small |

---

## Source Document
`CareerOS_CARE_RAG_Project_Idea.md` — full CARE-RAG specification at repo root.

*Related: [[active-goals]] · [[scoring-knowledge]] · [[architecture-index]]*
