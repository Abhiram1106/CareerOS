# Architecture Notes — CareerOS Campus AI

> Loaded by AI tools during architecture-type tasks (deep mode).
> More detailed than ADRs — captures how components actually fit together
> in practice, not just what was decided.

---

## System overview

```
Student Browser
    │
    ▼
apps/web (Next.js 14, :3000)
    │  lib/api.ts (typed fetch client)
    ▼
services/core-api (FastAPI, :8000)   ◄── JWT auth gate
    │         │            │
    ▼         ▼            ▼
ats-engine  ai-rewriter  (future services)
(:8001)     (:8003)      resume-parser (:8004)
                         match-engine  (:8005)
                         intel-bench   (CLI only)
    │
    ▼
PostgreSQL 16    Redis 7 (Celery broker + backend)
```

---

## Data flow — student scoring loop (Week 1–3)

```
1. Student uploads PDF/DOCX
   → POST /resumes/parse → services/resume-parser
   → returns resume_json (sections: summary, education, experience, projects, skills, por, certifications, links)
   → stored in resume_sections table

2. Student pastes JD
   → POST /scorecards → services/match-engine
   → TF-IDF cosine + embedding cosine + skill recall + eligibility rule
   → returns scorecard_json (6 components)
   → stored in scorecards table

3. Student requests rewrite
   → POST /rewrite → services/ai-rewriter
   → input: resume_json + jd_json + evidence_json + ats_flags
   → output: section_rewrites + unsupported_claims + requires_confirmation
   → stored in recommendations table

4. Student exports PDF
   → POST /resumes/export → core-api → Celery task → WeasyPrint
   → returns PDF download
```

---

## Data flow — officer cohort loop (Week 4)

```
1. Officer creates batch (college + dept + grad_year)
   → POST /batches → stored in batches table

2. Officer uploads 20 resumes OR students self-upload
   → each resume goes through the student scoring loop above
   → batch_resumes join table links them

3. Officer views dashboard
   → GET /officer/dashboard?batch_id=X
   → aggregates: readiness buckets, dept breakdown, top skill gaps, parse-safe %
   → rendered in apps/web/app/(officer)/dashboard/

4. Officer exports readiness report
   → POST /officer/report → Celery → WeasyPrint PDF
```

---

## Scoring formula (single source: packages/scoring/)

```
PlacementReadinessScore =
  0.35 × JD_Match
  0.20 × ATS_Parse_Safety
  0.20 × Evidence_Quality
  0.10 × Profile_Completeness
  0.10 × Interview_Readiness
  0.05 × Placement_Hygiene

JD_Match =
  0.35 × TFIDF_Cosine
  0.35 × Embedding_Cosine
  0.20 × Required_Skill_Recall
  0.10 × Eligibility_Rule_Score

Buckets: 0–49 high-risk | 50–69 borderline | 70–84 ready | 85–100 strong
```

---

## Intel optimization layer (Week 5)

- Sentence-transformer inference: PyTorch baseline → OpenVINO IR (FP32 → FP16 → INT8)
- TF-IDF + cosine + KMeans: stock sklearn → sklearnex patch
- Benchmark harness: `services/intel-bench/run.py --workload all --size {small|medium|large}`
- Results consumed by `apps/web/app/lab/intel/` panel
- Rule: accuracy delta > 1% on match quality → stay at FP16, report honestly

---

## Database schema — key tables

```
users → session_tokens
users → career_profiles (one-to-one)
users → resumes → resume_sections
                → resume_evidence
resumes → scorecards ← job_descriptions
scorecards → recommendations
colleges → departments → students ← users
batches (college+dept+grad_year) → batch_resumes → resumes
events_audit (actor_id, action, target_id, ts, payload_json)
benchmark_runs (workload, baseline_ms, intel_ms, throughput, accuracy_delta)
```

---

## Key conventions

- **Route handlers are thin.** No logic beyond: parse input → call service → return.
- **All cross-service HTTP via `clients.py`.** Single place to add auth headers, timeouts, retries.
- **Alembic migrations are the only way to change schema.** `AUTO_CREATE_TABLES=false`.
- **Score formula imported from `packages/scoring/`.** Never inline.
- **`packages/contracts/schemas/*.json`** are the cross-language ground truth. Python mirrors them in Pydantic; TypeScript imports generated types from `packages/ts-types/`.

---

_Populate this file further as the architecture evolves. Update before each weekly milestone._
_Last updated: 2026-05-19 (Phase 2 scaffold)_
