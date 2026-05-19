# Project Context

- **Project Name**: CareerOS Campus AI
- **Current Goal**: Ship a 9+/10 Intel-optimized placement-readiness platform for Indian colleges, demoable in 3 minutes (5-week build).
- **Stack**: Next.js 14 (apps/web) + FastAPI (services/core-api, ats-engine, ai-rewriter) + PostgreSQL 16 + Redis 7 + Celery + WeasyPrint.
- **Package Manager**: pnpm 9 (JS workspaces); pip per service (Python).
- **Project Type**: Hybrid polyglot monorepo (small-team variant per `deep-research-report (1).md`).
- **Architecture**:
  - Student loop: upload PDF/DOCX → `services/resume-parser` (Week 1) → structured JSON → `services/match-engine` (Week 2) hybrid TF-IDF + embedding + skill recall + eligibility vs pasted JD → 6-component PlacementReadinessScore → `services/ai-rewriter` (Week 3) proof-linked rewrite → WeasyPrint PDF export.
  - Officer loop: batch upload → `apps/web/(officer)/dashboard` (Week 4) → readiness heatmap, review queue, skill-gap chart, dept breakdown, readiness PDF report.
  - Intel layer: `services/intel-bench` (Week 5) measures OpenVINO + sklearnex speedups vs PyTorch/stock-sklearn baselines.
- **Important Constraints**:
  - No public job board, no scraping, no LinkedIn import (research §"LinkedIn and external API risk").
  - No recruiter side, no billing — explicitly cut.
  - No fabrication in AI rewriter — proof-linked, schema-constrained.
  - Real measured Intel benchmarks only; no vendor-headline claims.
  - DPDP-aware design (RBAC + audit logs + retention hooks); legal review out of MVP scope.
- **Current Priorities**: Week 1 step 3 — real Alembic delta migration + role claim in JWT + resume upload endpoint + `pdfplumber`/`python-docx` parser stub.
- **Known Risks**:
  - PDF parsing fragility on Indian fresher resumes (Canva, two-column, scanned).
  - OpenVINO INT8 conversion may degrade match accuracy → ship FP16 if so.
  - No real pilot data in 5 weeks → demo on synthetic + hand-labeled cohort, frame outcome lift as next step.
- **Active Decisions**: see `04-DECISIONS/decisions.md`. Key ones:
  - Hybrid monorepo (small-team variant) — ADR 0002.
  - Pivoted from broad "AI careers platform" to placement-readiness operating layer — ADR 0001.
  - All work on `main`; archive branch on origin preserves pre-cut MVP.
- **Known Errors**: see `03-ERRORS/error-memory.md`.
- **Do Not Repeat**: see `03-ERRORS/anti-patterns.md`.
- **Next Steps**:
  1. Write real Alembic delta migration adding colleges/departments/resume_sections/resume_evidence/job_descriptions/scorecards/recommendations/batches/batch_resumes/events_audit/benchmark_runs.
  2. Add `role` claim to JWT and gate routes by `student` / `officer` / `admin`.
  3. Implement `services/resume-parser` (pdfplumber + python-docx + section extractor).
  4. Wire `apps/web/(student)/resume/` to call the new parser and render extracted sections.

---
_Last updated: 2026-05-19 by Phase 2 restructure session._
