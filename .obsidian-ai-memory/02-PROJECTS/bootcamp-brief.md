---
tags: [bootcamp, intel, demo, pitch]
type: project
updated: 2026-05-21
links: [_INDEX, MASTER_PLAN, intel-index, scoring-knowledge]
---

# Intel AI Bootcamp — CareerOS Campus AI Project Brief

← [[_INDEX]] · [[MASTER_PLAN]] · [[intel-index]] · [[scoring-knowledge]]

> This document is the single source of truth for the bootcamp context.
> Read this before every session involving pitch, demo, scoring, or Intel integration.

---

## What is this project? (30-second version)

**CareerOS Campus AI** is an AI-powered placement-readiness platform for Indian colleges, built specifically for the **Intel AI Bootcamp**.

It uses **Intel hardware and Intel AI tools** (OpenVINO, sklearnex) to run a pipeline that:
1. Parses student resumes (PDF/DOCX)
2. Scores them against a real company job description
3. Gives AI-generated, proof-linked improvement suggestions
4. Shows the placement officer a live cohort readiness dashboard

**The Intel connection is real and specific** — not a sticker. The matching and analytics pipelines are benchmarked on Intel CPUs using OpenVINO for inference and Intel Extension for Scikit-learn for analytics workloads.

---

## Why was this project chosen for the bootcamp?

The bootcamp judges score on:

| Criterion | Why CareerOS scores high |
|---|---|
| Problem severity | 42.6% of Indian graduates are not employable (Mercer Mettl 2025). Real, massive, measurable pain. |
| Demo potential | Upload resume → score → rewrite → officer dashboard → Intel benchmark. Visual, before/after, 3 minutes. |
| Intel relevance | OpenVINO for embedding inference, sklearnex for TF-IDF + KMeans. Real benchmarks measured on hardware. |
| Technical depth | 6-service monorepo, Alembic migrations, Pydantic v2, Celery, real parsing pipeline, proof-linked LLM guardrails. |
| Social impact | Directly addresses India's placement cell workflow problem at scale. |
| Business potential | B2B SaaS sold to TPO offices. No job board dependency. Institutional, sticky buyer. |
| Pitch clarity | One sharp positioning: "placement-readiness operating layer for Indian colleges." Not "AI resume builder." |

---

## The problem being solved

### Context: Indian college placements

- India has **4.33 crore** higher-education enrolments (AISHE 2021–22)
- **8.47 lakh** engineering/B.Tech graduates pass out every year
- Only **42.6%** of graduates who apply for jobs are considered overall employable (Mercer | Mettl 2025 India Graduate Skill Index)
- The ILO India Employment Report 2024 confirms educated youth face the **highest unemployment** due to skill-job mismatch

### Why placement cells can't fix it today

Every Indian college has a **Training & Placement Office (TPO)**. They coordinate all company drives: resume submission, shortlisting, tests, GDs, interviews, offer management.

Today they do it with:
- WhatsApp groups for resume collection
- Excel sheets for eligibility tracking
- Manual one-by-one resume review
- Zero aggregate analytics on which department is weakest before TCS/Infosys arrives

**CareerOS gives them the operating layer they never had.**

### Why individual resume tools don't solve it

Jobscan, Rezi, Naukri tools, Internshala — all are consumer/student-first. None of them have:
- Batch cohort upload and analysis
- Department-level heatmaps
- Proof-linked officer approval queues
- Intel-measured inference pipelines
- Company-specific fit scoring before a drive

---

## Who uses it? (3 personas)

### 1. Student — Priya (CSE final year, 3 days before Accenture drive)
- Uploading her Canva two-column resume
- Doesn't know it will fail ATS parsing because of the multi-column layout
- Has no idea SQL is the #1 missing keyword for the JD
- Wants: upload → instant feedback → specific fixes → ATS-safe export

### 2. Placement Officer / TPO — Mr. Ramesh
- Managing 400 students across 6 departments
- Currently reviewing resumes in WhatsApp + Excel
- Needs: one dashboard → who is ready, who is at risk, what skills the batch is missing
- Needs: approval queue with proof-linked review, export report for the dean

### 3. College Admin / TPO Head — Dr. Mehta
- Responsible for annual placement report to management
- Needs: longitudinal data, department comparisons, training ROI evidence
- Uses the system monthly, not daily

---

## The Intel integration (the technical differentiator)

### Why Intel tools specifically

The core bottleneck in CareerOS is the **matching and analytics pipeline** — running TF-IDF, cosine similarity, semantic embeddings, and KMeans clustering on hundreds to thousands of resumes per batch. These workloads are:
- **CPU-bound** (exactly where Intel CPUs + acceleration libraries shine)
- **Parallelizable** (batch processing)
- **Latency-sensitive** (placement officer waits for results)

### What Intel tools are used

| Tool | Where used | Why |
|---|---|---|
| **OpenVINO** | `services/match-engine/` — embedding inference | Converts sentence-transformer model to IR format (FP16), runs 2.5× faster on Intel CPU than PyTorch baseline |
| **Intel Extension for Scikit-learn (sklearnex)** | `services/match-engine/` — TF-IDF, cosine, KMeans | Patches sklearn estimators at runtime; 4× faster KMeans clustering on batch analytics |
| **Intel oneDAL** | `services/intel-bench/` — data analytics | Optional acceleration for preprocessing, PCA, batch transforms |

### How to use sklearnex (critical — apply before any sklearn import)

```python
from sklearnex import patch_sklearn
patch_sklearn()  # must be BEFORE all sklearn imports
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```

### OpenVINO conversion pattern

```python
from openvino.runtime import Core

core = Core()
model = core.read_model("model/embedding_model.xml")
compiled = core.compile_model(model, "CPU")
# Measure accuracy delta vs PyTorch baseline before shipping
# If accuracy_delta > 0.01 on match quality → stay at FP16, never INT8
```

### Benchmark methodology (must be real numbers)

Run at three dataset sizes:
- **Small**: 500 resumes, 50 JDs
- **Medium**: 5,000 resumes, 300 JDs
- **Large**: 20,000 resumes, 1,000 JDs

Report per workload:
- `p50_latency_ms` — median latency
- `p95_latency_ms` — tail latency
- `throughput_rph` — resumes per hour
- `accuracy_delta` — score difference vs baseline (must be < 0.01)
- `memory_mb` — peak memory footprint
- `hw_label` — exact CPU model and RAM

**Never use vendor headline numbers. Only measured numbers from the actual hardware.**

---

## The 3-minute demo script (judge-facing)

> This is the single most important thing to practice. Judges score demo quality heavily.

**Scene 1 — Officer dashboard (start here, not with login)**
> "Today our college has an Accenture ASE placement drive. I paste the JD."

**Scene 2 — Batch upload**
> "I upload 20 student resumes from CSE final year."

**Scene 3 — Intel-optimized processing**
> "The system parses each resume, extracts skills and projects, runs JD similarity scoring using Intel-accelerated TF-IDF and sentence-transformer embeddings."

**Scene 4 — Dashboard result**
> Show: 20 scanned · 6 ready · 9 borderline · 5 high-risk · top missing skills: SQL, REST API, Git, OOP · avg readiness: 62%

**Scene 5 — Student fix**
> Open one low-scoring student (score: 48 → High Risk).
> Show: missing skills highlighted · ATS issue (two-column) · weak project bullets.
> Click "Rewrite with verified evidence."
> Show: one unsupported claim REFUSED ("Led a 5-member team" → no evidence).
> Show: two bullets improved.
> Score lifts: 48 → 73 (Borderline → Ready).

**Scene 6 — Intel panel**
> "The same pipeline — baseline PyTorch vs OpenVINO + sklearnex."
> Show: p50 latency table · throughput chart · accuracy delta < 0.5%.

**Total: under 3 minutes.**

---

## What this project is NOT (never pitch these)

- Not a job board
- Not a recruiter marketplace (NEXUS ATS was cut — see archive branch)
- Not a LinkedIn scraper or importer (API terms restrict this)
- Not a billing/subscription product (cut)
- Not "just another resume builder"
- Not a mobile app
- Not a 500,000-concurrent-user enterprise claim

---

## Scoring formula (the 9+/10 formula)

```
PlacementReadinessScore =
  0.35 × JD_Match
  0.20 × ATS_Parse_Safety
  0.20 × Evidence_Quality
  0.10 × Profile_Completeness
  0.10 × Interview_Readiness
  0.05 × Placement_Hygiene

JD_Match =
  0.35 × TFIDF_Cosine          (lexical keyword overlap)
  0.35 × Embedding_Cosine      (semantic similarity, OpenVINO-accelerated)
  0.20 × Required_Skill_Recall (fraction of JD required skills found in resume)
  0.10 × Eligibility_Rule_Score (CGPA, branch, backlogs, grad year hard filters)
```

**Buckets:**
- 0–49 → 🔴 High Risk
- 50–69 → 🟡 Borderline
- 70–84 → 🟢 Ready
- 85–100 → 🏆 Strong

**Single source of truth: `packages/scoring/`** — never duplicated in service code.

---

## Honest answers to hard judge questions

| Judge question | Correct answer |
|---|---|
| "Won't colleges just use Jobscan?" | Jobscan is consumer/student-first. It has no batch analytics, no officer dashboard, no cohort heatmaps, no proof-linked approval queue. It can't tell a TPO which department is weakest before the drive. |
| "What is the moat?" | Not the formula. The moat is campus workflow integration + verified outcome data over time. We own the data layer that connects resume submission → shortlist → offer. |
| "Why is this an Intel project?" | The scoring and matching pipeline is CPU-bound and batch-parallel — exactly the workload Intel accelerates. We use OpenVINO for embedding inference and sklearnex for TF-IDF + KMeans. Benchmarks are measured on real hardware. |
| "What stops students gaming the AI?" | The rewriter is proof-linked and schema-constrained. Every suggestion must have `evidence_ids[]` pointing to resume content. Unsupported claims go into `unsupported_claims[]`, never into `section_rewrites[]`. |
| "Can you prove lift?" | In the demo: we show a score going from 48 → 73. In production: event logging from upload → shortlist → offer enables A/B comparison. We frame outcome data as the next milestone, not a current claim. |
| "Did you fabricate the benchmark numbers?" | No. We measure on [specific CPU model], report p50/p95 latency, throughput, accuracy delta. If the accuracy delta is > 1%, we don't ship INT8 — we stay at FP16 and say so honestly. |
| "Is this just a resume builder?" | It's a placement-office operating system. The resume builder is one student-facing feature. The product center is the officer dashboard and cohort intelligence. |

---

## 5-week timeline (bootcamp schedule)

| Week | Focus | Key deliverable | Demo-able? |
|---|---|---|---|
| 1 ✅ | Foundation | Alembic migration · role auth · resume upload + pdfplumber parser · enterprise frontend shell + Motion animations | Upload PDF → see extracted sections |
| 2 🔨 | Scoring | JD parser · services/match-engine (TF-IDF + embeddings + sklearnex) · packages/scoring/ · score breakdown UI | Paste JD → 6-bar PlacementReadinessScore |
| 3 | AI rewriter | services/ai-rewriter proof-linked rewrite · before/after UI · WeasyPrint PDF export | Apply rewrite → unsupported claim refused → score lift |
| 4 | Officer surface | apps/web/(officer)/ · dept heatmap · review queue · batch upload · readiness PDF | 20 resumes vs 1 JD → full cohort dashboard |
| 5 | Intel + pitch | services/intel-bench · /lab/intel panel · 6-slide pitch deck · 3-min demo script | Side-by-side latency/throughput benchmark chart |

---

## Pitch deck outline (6 slides, Week 5 deliverable)

1. **Problem** — 42.6% employability · 8.47L graduates/year · manual TPO workflows
2. **Why tools fail** — consumer-first, no cohort intelligence, no batch workflow
3. **Solution** — student score + officer dashboard + Intel-measured inference
4. **Intel relevance** — OpenVINO + sklearnex · real benchmarks · CPU-native pipeline
5. **Early proof** — score lift demo · parse-safe uplift · benchmark chart
6. **Wedge and moat** — campus workflow integration → outcome data → defensible

---
*Last updated: 2026-05-21*

*Related: [[_INDEX]] · [[MASTER_PLAN]] · [[intel-index]] · [[scoring-knowledge]] · [[02-PROJECTS/project-context]] · [[architecture-index]]*
