# CareerOS — Career Intelligence Platform

An AI-powered career platform for Indian students and freshers: resume parsing, multi-system ATS scoring, JD matching with sentence embeddings, proof-linked rewrites, job search, and a structured career profile.

**Product doc:** `CareerOS_Complete_Documentation.md` — full SRS/PRD/FRD/BRD.
**Teammate onboarding:** `docs/handoff/` — start with `README.md`.

---

## Quick start

```bash
git clone <repo> && cd CareerOS
docker compose up -d --build     # all 9 backend services
cd apps/web && pnpm install && pnpm dev   # frontend :3000
```

App: http://localhost:3000 · API docs: http://localhost:8000/docs

---

## Repo layout

```
apps/
  web/                  Next.js 14 — student UI
services/
  core-api/             FastAPI — auth, profile, scoring, orchestration
  resume-parser/        PDF/DOCX → structured sections + ATS flags
  match-engine/         TF-IDF + MiniLM embeddings + skill matching
  ats-engine/           7-dimension ATS parse-safety analyzer
  ai-rewriter/          Proof-linked rule-based resume rewriter
  jobs-feed/            Adzuna API + seed fallback
    seed/               jobs.seed.json — 12 seed job listings
  intel-bench/          Performance benchmark harness
packages/
  scoring/              PlacementReadinessScore formula (single source of truth)
tests/
  golden/               Discrimination gate corpus + runner
docs/
  handoff/              Teammate knowledge-transfer (10 documents)
  benchmarks/           Intel performance measurements
  adr/                  Architecture decision records
.claude/                Claude Code config + rules
.cursor/                Cursor AI config + rules
.obsidian-ai-memory/    Engineering memory vault (sessions, errors, decisions)
.github/workflows/      CI (temporarily disabled — workflow_dispatch only)
```

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14, TypeScript strict, CSS variables |
| API | FastAPI 0.115, SQLAlchemy 2.0, Pydantic v2, Celery |
| Database | PostgreSQL 16 + Redis 7 |
| Embeddings | sentence-transformers all-MiniLM-L6-v2 (384-dim, 24ms p50) |
| Intel layer | sklearnex TF-IDF acceleration, OpenVINO path wired |
| PDF export | WeasyPrint (ATS-safe, text-selectable) |
| Auth | JWT + SessionTokens, bcrypt, password reset |

---

## What's implemented

- ✅ Structured career profile (WorkExperience, Education, Skills, Projects, Certifications, JobApplications)
- ✅ Resume upload → parse → ATS flags → 7-dimension safety score
- ✅ JD matching (TF-IDF + MiniLM semantic cosine + skill recall + eligibility)
- ✅ 6-component PlacementReadinessScore with discrimination gate 5/5 PASS
- ✅ Proof-linked rewriter (STAR verb upgrade, filler removal, anti-fabrication)
- ✅ Job search (Adzuna API + 12-job seed fallback)
- ✅ Full profile editor UI (all structured sections with add/edit/delete)
- ✅ Password reset, CI workflow, Intel benchmarks

**Next:** Resume builder (3 ATS-safe templates), multi-vendor ATS simulation, application tracker UI.

---

## Validation

```bash
# TypeScript
cd apps/web && npx tsc --noEmit

# Discrimination gate (runs inside core-api container)
docker compose cp tests/golden/corpus.py core-api:/tmp/corpus.py
docker compose cp tests/golden/_runner.py core-api:/tmp/_runner.py
docker compose exec core-api python /tmp/_runner.py

# Python syntax
find services packages -name "*.py" -exec python -c "import ast; ast.parse(open('{}').read())" \;
```

---

## Database migrations

| File | What |
|---|---|
| `0001_student_baseline.py` | Core tables (users, resumes, scorecards, etc.) |
| `0002_profile_eligibility_fields.py` | cgpa, active_backlogs, branch, grad_year |
| `0003_structured_profile.py` | WorkExperience, Education, Skills, Projects, Certifications, JobApplications |

```bash
docker compose exec core-api alembic upgrade head
```
