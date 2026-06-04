---
tags: [project, context, care-rag, platform]
type: project
updated: 2026-06-04
links: [_INDEX, MASTER_PLAN, scoring-knowledge, architecture-index, care-rag-architecture]
---

# Project Context — CareerOS: CARE-RAG Career Intelligence Platform

← [[_INDEX]] · [[MASTER_PLAN]] · [[care-rag-architecture]]

---

## What CareerOS is

**CareerOS** is a continuously improving AI career intelligence platform powered by **CARE-RAG** (Continuous Adaptive Resume Enhancement using Retrieval-Augmented Generation).

It is **not** a resume builder. It is **not** an ATS checker. It is a learning career operating system that gets smarter with every resume uploaded, every JD matched, every suggestion accepted, and every placement outcome recorded.

**One-line pitch:**
> CareerOS is a self-improving AI career platform that learns from resumes, job descriptions, and hiring outcomes to help candidates build better resumes, pass ATS filters, and find the right jobs.

**Primary market:** Indian students, freshers, early-career professionals.

---

## The Problem

Every year, millions of qualified candidates in India are rejected not because they lack skills — but because their resumes fail automated screening software before a human ever reads them. 75–88% of resumes submitted to large employers are filtered out by ATS before review.

The gap competitors miss: not just resume improvement, but **career intelligence that compounds over time**.

---

## The CARE-RAG Advantage

Most tools solve: *"Here is your resume. Here is a JD. Improve keywords."*

CareerOS solves: *"Across thousands of resumes, job descriptions, edits, and placement outcomes — what actually makes a candidate visible, shortlisted, and interview-ready for a specific role?"*

---

## Architecture: 7-Layer CARE-RAG Pipeline

```
Resume + JD Upload
    ↓ Layer 1: Structured Ingestion
    ↓ Layer 2: 7-Class Quality Classification
    ↓ Layer 3: Multi-Index Knowledge Base (vector store)
    ↓ Layer 4: Hybrid Retrieval (semantic + BM25 + skill graph + outcome)
    ↓ Layer 5: RAG Reasoning: Diagnose → Compare → Recommend → Rewrite → Verify
    ↓ Layer 6: Feedback Learning Loop
    ↓ Layer 7: Evaluation + Guardrail (confidence, provenance, truthfulness)
    ↓
Job Search → Outcome Tracking → Knowledge Base Improvement
```

See [[care-rag-architecture]] for the full layer-by-layer breakdown.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, TypeScript strict, CSS variables |
| API | FastAPI 0.115, SQLAlchemy 2.0, Pydantic v2, Celery |
| Database | PostgreSQL 16 + Redis 7 |
| Embeddings | MiniLM all-MiniLM-L6-v2 (384-dim, 24ms p50, 148K pairs/hr) |
| Vector store | ChromaDB (planned M9 — embedded, no external API) |
| ATS simulation | 7-vendor weighted simulation (Taleo, Workday, Naukri RMS, Greenhouse, PeopleStrong, Darwinbox, Lever) |
| Intel layer | sklearnex TF-IDF acceleration; OpenVINO path wired for embeddings |
| PDF export | WeasyPrint (ATS-safe, text-selectable) |
| Auth | JWT + SessionTokens + bcrypt + password reset |

---

## Scoring Formula (single source: packages/scoring/)

```
PlacementReadinessScore =
  0.35 × JD_Match
+ 0.20 × ATS_Parse_Safety
+ 0.20 × Evidence_Quality
+ 0.10 × Profile_Completeness
+ 0.10 × Interview_Readiness
+ 0.05 × Placement_Hygiene

JD_Match =
  0.35 × TFIDF_Cosine           (sklearnex-accelerated)
+ 0.35 × Semantic_Cosine        (MiniLM embeddings)
+ 0.20 × Required_Skill_Recall  (70-skill taxonomy + 50 aliases)
+ 0.10 × Eligibility_Rule_Score (CGPA, backlogs, branch, grad year)
```

**7-Class quality classifier (planned M6):**

| Class | Meaning |
|---|---|
| ATS Broken | Parser cannot read the resume |
| Structurally Weak | Sections incomplete or missing |
| Keyword Weak | Skills present but not in resume text |
| Impact Weak | No measurable outcomes in bullets |
| Role Misaligned | Good resume, wrong role for this JD |
| High Potential, Underwritten | Has skills but resume doesn't show it |
| Interview Ready | ATS-safe, role-aligned, evidence-backed |

---

## What's Built vs Planned

### ✅ Built
- 9-container Docker stack (all services healthy)
- Resume parser (PDF/DOCX + OCR + structured sections)
- JD parser (skills + eligibility extraction)
- 7-dimension ATS analyzer + 7-vendor ATS simulation
- Keyword gap analysis with importance weights
- TF-IDF + MiniLM embedding JD match scoring
- Real eligibility scoring (CGPA/backlogs/branch/grad year vs JD)
- Proof-linked rule-based rewriter (anti-fabrication)
- 3 ATS-safe resume templates (classic/technical/fresher)
- Structured career profile (WorkExp/Education/Skills/Projects/Certs/JobApplications)
- Application tracker (kanban + list view)
- Score history sparkline + delta analytics
- Full profile editor UI
- CI workflow + discrimination gate 5/5

### 🔴 Building Now (M6–M8)
- 7-class resume quality classifier (deterministic, no new infra)
- JD intelligence heatmap UI (frontend only)
- Guided AI resume wizard (rule-based, 5-step flow)

### 🟡 Planned (M9–M12)
- ChromaDB vector store + multi-index knowledge base
- Hybrid retrieval + provenance-based suggestions
- Skill graph relationships
- Feedback loop wiring (outcome → knowledge base)
- Resume evolution timeline UI

### Post-MVP
- B2B college placement dashboard
- LinkedIn OAuth
- OpenVINO IR embeddings
- Interview preparation module
- Learning-to-rank model

---

## Constraints (always enforced)

- No fabrication — `unsupported_claims[]` gate on every rewrite
- Score formula only in `packages/scoring/` — never duplicated
- Real measured benchmarks only — no vendor headline numbers
- RBAC on every endpoint (`require_student`)
- tsc --noEmit + Python AST-parse clean before every commit
- Discrimination gate 5/5 before any scoring change
- Every AI suggestion must include confidence + evidence source

---

## Key Documents

- `CareerOS_Complete_Documentation.md` — full SRS/PRD/FRD/BRD
- `CareerOS_CARE_RAG_Project_Idea.md` — CARE-RAG full specification
- `docs/handoff/` — teammate onboarding (10 documents)
- [[care-rag-architecture]] — layer-by-layer CARE-RAG implementation map
- [[active-goals]] — current milestone tracker

---

_Updated: 2026-06-04 — Integrated CARE-RAG pipeline as the platform's AI architecture._

*Related: [[_INDEX]] · [[MASTER_PLAN]] · [[care-rag-architecture]] · [[active-goals]] · [[scoring-knowledge]]*
