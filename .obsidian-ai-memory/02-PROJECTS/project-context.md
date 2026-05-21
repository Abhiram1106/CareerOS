# Project Context

- **Project Name**: CareerOS Campus AI
- **Submission context**: Intel AI Bootcamp — final project. Scored on problem clarity, demo impact, Intel relevance, technical depth, social impact, and pitch quality. Target: 9+/10.
- **Deadline**: 5-week build from 2026-05-19. Week 1 complete. Week 2 in progress.
- **Current Goal**: Ship a demoable, Intel-optimized placement-readiness platform for Indian colleges. Score 9+/10 at the Intel AI Bootcamp.

---

## What the Intel judges care about

1. **Real Intel hardware usage** — OpenVINO for NLP inference, sklearnex for analytics. Benchmarks must be *measured on real hardware*, not vendor slides.
2. **Technically impressive but explainable** — judges can be non-technical. The demo must show a before/after story in under 3 minutes.
3. **Socially relevant** — Indian college placement is a real, evidence-backed problem (42.6% employability rate, ILO India Employment Report 2024).
4. **Demoable end-to-end** — upload resume → score → rewrite → officer dashboard → Intel panel. All visible in one session.
5. **Not a toy** — must feel production-grade. Real DB, real parsing, real scoring formula, real benchmarks.

---

## Stack

- **Web**: Next.js 14 (apps/web) — app router, TypeScript strict, no Tailwind, Motion animations
- **APIs**: FastAPI 0.115 (services/core-api, ats-engine, ai-rewriter, resume-parser)
- **Database**: PostgreSQL 16 + SQLAlchemy 2.0 + Alembic migrations
- **Queue**: Redis 7 + Celery (PDF export async task)
- **AI — Intel layer**:
  - OpenVINO: optimize sentence-transformer model for embedding inference
  - Intel Extension for Scikit-learn (sklearnex): patch TF-IDF, cosine, KMeans
  - Benchmarks: `services/intel-bench/` — p50/p95 latency, throughput, accuracy delta
- **AI — LLM layer**: proof-linked rewriter via LLM API (Claude/OpenAI) with strict JSON schema guardrails
- **Package manager**: pnpm 9 (JS) + pip per Python service

---

## Architecture

### Student loop (Weeks 1–3)
```
Upload PDF/DOCX
  → services/resume-parser  (pdfplumber + python-docx + spaCy section extractor)
  → structured JSON with sections + ATS flags
  → services/match-engine   (TF-IDF cosine + embedding cosine + skill recall + eligibility)
  → 6-component PlacementReadinessScore (packages/scoring/)
  → services/ai-rewriter    (proof-linked LLM rewrite, JSON schema, no fabrication)
  → WeasyPrint PDF export via Celery
```

### Officer loop (Week 4)
```
Create batch (college + dept + grad_year)
  → bulk upload resumes → all go through student loop
  → apps/web/(officer)/dashboard
    → readiness heatmap by department
    → top missing skills bar chart
    → review queue (approve / return with note)
    → company fit columns
    → export readiness PDF report
```

### Intel benchmark loop (Week 5)
```
services/intel-bench/run.py --workload all --size medium
  → baseline: PyTorch CPU + stock sklearn
  → Intel path: OpenVINO IR (FP16) + sklearnex patched
  → measures: p50 latency, p95 latency, throughput (resumes/hr), accuracy delta, memory MB
  → outputs: benchmark_runs.json → consumed by apps/web/app/lab/intel/
```

---

## PlacementReadinessScore formula (single source: packages/scoring/)

```
Score =
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
```

Buckets: 0–49 🔴 High Risk | 50–69 🟡 Borderline | 70–84 🟢 Ready | 85–100 🏆 Strong

---

## Important constraints

- No job board, no LinkedIn scraping, no recruiter marketplace — cut.
- No billing — cut.
- No fabrication in AI rewriter — unsupported claims go in `unsupported_claims[]`, never in `section_rewrites[]`.
- Real measured Intel benchmarks only — no vendor headline numbers.
- DPDP-aware design: RBAC + audit logs + retention hooks. Legal review deferred post-bootcamp.
- Score formula lives only in `packages/scoring/` — never duplicated in service code.

---

## Known risks

- PDF parsing fragility on Indian fresher Canva templates, two-column layouts, scanned resumes.
- OpenVINO INT8 may degrade match accuracy — fall back to FP16 if accuracy delta > 1%.
- No real pilot data — demo uses synthetic + hand-labeled corpus. Outcome lift framed as next step.

---

## Active decisions

- Hybrid monorepo (small-team variant) — ADR 0002.
- Pivoted from broad "AI careers platform" to placement-readiness layer — ADR 0001.
- All work on `main`; `origin/archive/pre-campus-ai` preserves pre-cut MVP.
- Omnix runtime stays at `.omnix/`; `platform/omnix/` is the documented future target.

---

## Known errors + anti-patterns

See `.obsidian-ai-memory/03-ERRORS/error-memory.md`
See `.obsidian-ai-memory/03-ERRORS/anti-patterns.md`

---

## Next steps

Week 2:
1. JD parser + skill taxonomy + eligibility extractor (`/jd/parse` endpoint)
2. `services/match-engine/` — TF-IDF + embeddings + recall + eligibility → JD_Match sub-score
3. `packages/scoring/` — PlacementReadinessScore Python package
4. Score breakdown UI in `apps/web` — 6-bar component + bucket label + missing skills list

## Layered architecture (refactor in progress)

- Vault: `.obsidian-ai-memory/05-ARCHITECTURE/layered-modules.md`
- Auth routes migrated to `api/controllers` + `modules/auth` (2026-05-21)
- Next migration: **resume + export**, then ATS/dashboard

---
_Last updated: 2026-05-21 — layered-modules vault + auth migration._
