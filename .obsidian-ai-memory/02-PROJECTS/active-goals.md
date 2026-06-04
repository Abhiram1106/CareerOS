---
tags: [project, goals, roadmap, careeros, care-rag]
type: project
updated: 2026-06-04
links: [MASTER_PLAN, _INDEX, scoring-knowledge, security-architecture]
---

# Active Goals — CareerOS: CARE-RAG Career Intelligence Platform

← [[MASTER_PLAN]] · [[_INDEX]]

> **Product vision (refined with CARE-RAG):**
> CareerOS is a continuously improving AI career intelligence platform powered by CARE-RAG
> (Continuous Adaptive Resume Enhancement using Retrieval-Augmented Generation).
> It analyzes resumes and job descriptions, classifies resume quality across 7 dimensions,
> retrieves successful patterns from a growing knowledge base, generates evidence-grounded
> improvements, and learns from user edits, application outcomes, and placement results.
> Primary market: Indian students, freshers, early-career professionals.

---

## ✅ Completed — Foundation (Phases 0–7)

### Core infrastructure
- [x] 9-container Docker stack (Postgres, Redis, Celery, core-api, resume-parser, match-engine, ats-engine, ai-rewriter, jobs-feed)
- [x] JWT auth + session tokens + password reset
- [x] Discrimination gate: 5/5 PASS (content-aware sub-scorers)
- [x] MiniLM all-MiniLM-L6-v2 sentence embeddings (24ms p50, 148K pairs/hr)

### CARE-RAG Layer 1 — Ingestion ✅
- [x] PDF/DOCX resume parser (pdfplumber + python-docx + OCR fallback)
- [x] Structured section extraction (education, experience, skills, projects, certifications)
- [x] JD text parser → required_skills, optional_skills, eligibility (CGPA/branch/backlogs/grad_year)
- [x] Structured career profile: WorkExperience, Education, Skill, Project, Certification, JobApplication
- [x] 24 REST CRUD endpoints + GET /profile/complete

### CARE-RAG Layer 2 — Quality Scoring (partial) ✅
- [x] 6-component PlacementReadinessScore (JD match 35%, ATS 20%, Evidence 20%, Completeness 10%, Interview 10%, Hygiene 5%)
- [x] 7-vendor ATS simulation (Taleo 18%, Workday 16%, Naukri RMS 15%, Greenhouse 12%, PeopleStrong 10%, Darwinbox 9%, Lever 8%)
- [x] Keyword gap analysis (JD keywords vs resume, importance-weighted)
- [x] 4-bucket score labels: high-risk / borderline / ready / strong

### CARE-RAG Layer 5 — Recommendations (partial) ✅
- [x] Proof-linked rewriter (STAR verb upgrade, filler removal, unsupported claim detection)
- [x] Anti-fabrication gate (unsupported_claims[], confidence scoring, no invention)
- [x] 3 ATS-safe resume templates (classic, technical, fresher) from structured profile

### CARE-RAG Layer 6 — Outcome Tracking (partial) ✅
- [x] JobApplication: saved → applied → screening → interview → offer/rejected
- [x] Score history: GET /analytics/score-history, sparkline, delta badge
- [x] EventAudit table (all significant actions logged)

### Frontend (M1–M5) ✅
- [x] M1: Full structured profile editor (Settings page)
- [x] M2: Resume builder with 3 templates reading from structured DB
- [x] M3: Vendor ATS simulation UI + keyword gap chips
- [x] M4: Application tracker (kanban + list view)
- [x] M5: Score history sparkline on dashboard

---

## 🔴 Active — CARE-RAG Adaptation Sprint

### M6 — 7-Class Resume Quality Classifier ✅ DONE
> CARE-RAG Layer 2: replaces 4-bucket labels with diagnostic classifications.
> Computed deterministically from existing scores — no new services needed.

**7 classes:**
| Class | Detection Logic |
|---|---|
| ATS Broken | ats_parse_safety < 40 OR has table_detected + two_column flags |
| Structurally Weak | profile_completeness < 40 + missing_standard_headings flag |
| Keyword Weak | jd_match < 40 AND required_skill_recall < 30 |
| Impact Weak | evidence_quality < 40 (no metrics, no strong verbs) |
| Role Misaligned | jd_match < 35 despite ats_parse_safety > 65 |
| Interview Ready | overall_score >= 70 |
| High Potential Underwritten | ats_parse_safety >= 65 AND evidence_quality < 40 |

- [ ] Add `classify_resume_quality(scores) → QualityClass` to `packages/scoring/formula.py`
- [ ] Inject `quality_class` into every scorecard response
- [ ] Replace bucket badge on /match page with diagnostic class label + fix guidance
- [ ] Add class to GET /analytics/score-history for evolution timeline
- **Files:** `packages/scoring/careeros_scoring/formula.py`, `services/core-api/app/modules/scorecard/mutation/score_resume_handler.py`, `apps/web/app/(app)/match/page.tsx`

### M7 — JD Intelligence Heatmap UI ✅ DONE
> CARE-RAG Layer 5: surface the JD keyword analysis as a visual heatmap.
> Keyword gap analysis already returns data — just needs better UI.

- [ ] Heatmap cards: each JD keyword shown as chip with colour intensity (green=present, amber=partial, red=missing)
- [ ] Keyword frequency badge (how many times it appears in JD)
- [ ] "Skill vs resume gap" separation: "You have this skill but didn't mention it" vs "You don't have this skill"
- [ ] Role alignment indicator: which role family this JD belongs to
- **Files:** `apps/web/app/(app)/match/page.tsx`, `apps/web/components/workspace/KeywordHeatmap.tsx` (new)

### M8 — Guided AI Resume Wizard ✅ DONE
> CARE-RAG Layer 5: conversational Diagnose→Compare→Recommend→Rewrite flow.
> Rule-based wizard using existing scores + structured profile. No LLM required for MVP.

- [ ] Step 1 Diagnose: show quality_class + top 3 issues from scorecard
- [ ] Step 2 Compare: "Strong resumes for this role typically have..." (static role-based patterns)
- [ ] Step 3 Recommend: prioritised fix list with estimated score improvement per fix
- [ ] Step 4 Rewrite: apply proof-linked rewriter to selected sections
- [ ] Step 5 Verify: re-score and show before/after delta
- **Files:** `apps/web/app/(app)/resume/wizard/page.tsx` (new), `services/ai-rewriter/`

### M9 — Vector Store + Resume Pattern Retrieval ✅ DONE
> CARE-RAG Layers 3+4: persistent knowledge base + hybrid retrieval.
> This is the structural core that enables evidence-grounded suggestions.

**Architecture:**
- New service: `services/vector-store/` using ChromaDB (lightweight, no external API)
- Every scored resume (quality_class >= "interview_ready") → embed + store in Resume Pattern Index
- Every parsed JD → embed + store in JD Intelligence Index
- At rewrite time: retrieve top-5 similar high-scoring resumes for the same role family
- Rewriter uses retrieved patterns as grounding context (replaces pure rule-based)

**Indexes:**
- `resume_patterns`: resume text chunks, quality_class, role, score, anonymised
- `jd_intelligence`: JD text, role family, extracted skills, keyword weights
- `user_memory`: per-user resume history, skill growth, accepted/rejected suggestions

- [ ] Add `services/vector-store/` with ChromaDB + FastAPI
- [ ] Embed + store every scorecard (when quality_class is known) on score completion
- [ ] Retrieval endpoint: GET /vector/similar-resumes?role=X&quality=interview_ready
- [ ] Inject retrieved patterns into proof_linked_rewrite_handler as context
- [ ] Add provenance to suggestions: "Based on 12 strong {role} resumes in our knowledge base"

### M10 — Skill Graph Index (MEDIUM)
> CARE-RAG Layer 3D: skill relationships for smarter gap analysis.

- [ ] Define skill graph: `React → JavaScript → Frontend → REST API → UI Components`
- [ ] `Python → Pandas → SQL → Dashboard → Data Analyst`
- [ ] `Java → Spring Boot → REST API → Backend Developer`
- [ ] Store as adjacency dict in `skill_taxonomy.py`
- [ ] Use graph to suggest adjacent skills: "You know Python — consider adding Pandas/SQL"
- [ ] Weight missing skills by graph distance from known skills

### M11 — Feedback Loop Wiring (MEDIUM)
> CARE-RAG Layer 6: close the learning loop.

- [ ] When recommendation is accepted → log to EventAudit with `care_rag.suggestion.accepted`
- [ ] When JobApplication moves to `interview` or `offer` → tag source scorecard as positive outcome
- [ ] Expose accepted/rejected counts on each Recommendation row
- [ ] Use positive outcome scorecards to populate Resume Pattern Index (M9) preferentially
- [ ] Surface: "X students with similar profiles got interviews after making this change"

### M12 — Resume Evolution Timeline UI (LOW)
> CARE-RAG §7.3: show score trajectory across resume versions.

- [ ] Version each generated resume with a label (v1, v2, v3)
- [ ] Timeline view: date → quality_class → overall_score for each version
- [ ] Before/after comparison: side-by-side score bars for any two versions
- [ ] "You improved from ATS Broken → Interview Ready in 3 edits"

---

## 🟡 Post-MVP

- [ ] B2B college portal — placement officer dashboard, cohort heatmaps, dept analytics (CARE-RAG §7.6)
- [ ] LinkedIn OAuth — profile import into structured career sections (CARE-RAG Layer 1)
- [ ] Google OAuth sign-in
- [ ] Recruiter database access module
- [ ] Job alerts + email notifications
- [ ] Cover letter generator (CARE-RAG Layer 5 extension)
- [ ] Interview preparation from resume + JD (CARE-RAG §8 V3)
- [ ] OpenVINO IR model for embedding inference
- [ ] Learning-to-rank model (CARE-RAG V3 — train on outcome data)
- [ ] Fine-tuned resume quality classifier (CARE-RAG V3)
- [ ] Placement prediction model

---

## Cross-cutting — always in scope

- [ ] RBAC on every new endpoint (`require_student`)
- [ ] No secrets in git; `.env.example` placeholders only
- [ ] PlacementReadinessScore only in `packages/scoring/`
- [ ] No fabrication in rewriter (`unsupported_claims[]`)
- [ ] tsc --noEmit clean before every commit
- [ ] Python AST-parse clean on all touched services
- [ ] Discrimination gate 5/5 before any scoring change
- [ ] Every AI suggestion must include confidence score + evidence source (CARE-RAG Layer 7)

---

_Updated: 2026-06-04 — Integrated CARE-RAG pipeline. M6–M12 replace old M6+post-MVP list._
_CARE-RAG full document: `CareerOS_CARE_RAG_Project_Idea.md` at repo root._

*Related: [[MASTER_PLAN]] · [[_INDEX]] · [[scoring-knowledge]] · [[05-ARCHITECTURE/security-architecture]]*
