---
tags: [hub, architecture, moc, system-design]
type: moc
created: 2026-05-21
updated: 2026-05-21
links: [_INDEX, MASTER_PLAN, api-index, scoring-knowledge, intel-index]
---

# 🏗️ Architecture Index — MOC

> Map of Content for all system design knowledge.  
> Hub-and-spoke: this note links every architectural document.

← [[_INDEX]] | ← [[MASTER_PLAN]] | [[api-index]] → | [[scoring-knowledge]] →

---

## 🗺️ System Overview

```
                    ┌─────────────────────┐
                    │   apps/web (:3000)   │  Next.js 14 + TypeScript
                    │  Student | Officer   │
                    └──────────┬──────────┘
                               │ JWT
                    ┌──────────▼──────────┐
                    │ core-api (:8000)     │  FastAPI + SQLAlchemy 2.0
                    │ api/router.py        │  Alembic + Celery
                    └──┬──────┬──────┬───┘
                       │      │      │
              ┌────────▼┐  ┌──▼───┐  ┌▼──────────┐  ┌──────────────┐
              │ats-engine│  │resume│  │ai-rewriter │  │match-engine  │
              │  :8001   │  │parser│  │  :8003     │  │  :8005 (W2)  │
              │          │  │:8004 │  │            │  │              │
              └──────────┘  └──────┘  └────────────┘  └──────────────┘
                                                        intel-bench (CLI)
              PostgreSQL 16 · Redis 7 (Celery broker)
```

→ Full diagram at [[05-ARCHITECTURE/README]]

---

## 📂 Architecture Documents

### Core Design
- [[05-ARCHITECTURE/README]] — System diagram, data flows, scoring formula, key tables
- [[05-ARCHITECTURE/layered-modules]] — 7-phase refactor map (all phases complete)
- [[05-ARCHITECTURE/frontend-ux]] — UI surfaces, components, CSS token system

### Data Model (key tables)
| Table | Purpose | Links |
|-------|---------|-------|
| `users` | Auth, role claim | → [[api-index#Auth Endpoints]] |
| `career_profiles` | Student profile | → [[api-index#Profile Endpoints]] |
| `resumes` + `resume_sections` | Parsed resume | → [[api-index#Resume Endpoints]] |
| `job_descriptions` | JD store | → [[api-index#JD Endpoints]] |
| `scorecards` | 6-component score | → [[scoring-knowledge]] |
| `recommendations` | AI rewrite output | → [[api-index#Rewriter Contract]] |
| `batches` + `batch_resumes` | Officer cohorts | → [[MASTER_PLAN#Week 4]] |
| `benchmark_runs` | Intel bench data | → [[intel-index#Benchmark Schema]] |
| `events_audit` | DPDP audit log | — |

→ See [[04-DECISIONS/decisions#Decision 2]] for monorepo structure rationale.

---

## 🧱 Layered Architecture (Phases 1–7 Complete)

```
Write path:   Frontend → Controller → Handler → Repo → Entity → DB
Read path:    Frontend ← Controller ← QueryService ← View ← Entity ← DB
```

### Phase Status
| Phase | Domain | Status | Notes |
|-------|--------|--------|-------|
| 1 | Scaffold | ✅ Done | Folder structure created |
| 2 | Auth | ✅ Done | `/auth/register`, `/auth/login` |
| 3 | Profile | ✅ Done | `GET/PUT /profile` |
| 4 | Resume + Export | ✅ Done | `/resumes/*`, `/resumes/export/*` |
| 5 | ATS + Dashboard | ✅ Done | `/ats/scan`, `/dashboard` |
| 6 | Frontend modules | ✅ Done | `lib/api.ts` canonical, no inline fetch |
| 7 | Satellite scaffold | ✅ Done | ats-engine, resume-parser, ai-rewriter |

→ Full phase map at [[05-ARCHITECTURE/layered-modules]]  
→ Session trail: [[01-SESSIONS/2026-05-21/session-1700-cursor]], [[01-SESSIONS/2026-05-21/session-1800-cursor]], [[01-SESSIONS/2026-05-21/session-phases-4-7-cursor]]

---

## 🛣️ Data Flows

### Student Scoring Loop
```
Student uploads PDF/DOCX
→ resume-parser (:8004) — pdfplumber + python-docx + spaCy
→ resume_sections table (section_name, content_json, confidence)
→ Student pastes JD text
→ match-engine (:8005) — TF-IDF + embeddings + recall + eligibility  ← Week 2
→ scorecards table (6-component score)
→ Score breakdown UI in /workspace
→ [optional] ai-rewriter (:8003) — proof-linked JSON rewrite
→ WeasyPrint PDF export via Celery
```

### Officer Cohort Loop
```
Officer creates batch → uploads N resumes → attaches JD
→ Batch Celery task → score all resumes
→ batch_resumes table updated
→ dashboard: dept heatmap, top skill gaps, readiness buckets
→ review queue: proof-linked approve / return
→ Export readiness PDF report
```

### Intel Benchmark Loop
```
services/intel-bench/run.py --workload all --size medium
→ Baseline: stock sklearn + PyTorch
→ Intel: sklearnex.patch_sklearn() + OpenVINO FP16 compiled model
→ benchmark_runs.json → /lab/intel page
→ p50/p95 latency · throughput (RPH) · accuracy_delta · memory_mb
```

→ Intel details at [[intel-index]] · Scoring formula at [[scoring-knowledge]]

---

## 🗂️ Service Registry

| Service | Port | Tech | Status | Layered? |
|---------|------|------|--------|----------|
| `core-api` | 8000 | FastAPI + SQLAlchemy 2.0 | ✅ Running | ✅ Phases 1–7 |
| `ats-engine` | 8001 | FastAPI | ✅ Running | ✅ Phase 7 scaffold |
| `ai-rewriter` | 8003 | FastAPI + LLM | ✅ Running | ✅ Phase 7 scaffold |
| `resume-parser` | 8004 | FastAPI + pdfplumber | ✅ Running | ✅ Phase 7 scaffold |
| `match-engine` | 8005 | FastAPI + sklearnex | ⏳ Week 2 | — |
| `intel-bench` | CLI | Python harness | ⏳ Week 5 | — |

→ Client wiring at [[api-index#Service Clients]]

---

## 🏛️ Decisions Affecting Architecture

1. [[04-DECISIONS/decisions#Decision 1]] — Pivot to Campus AI (cut recruiter/billing/job-board)
2. [[04-DECISIONS/decisions#Decision 2]] — Hybrid small-team monorepo structure
3. [[04-DECISIONS/decisions#Decision 3]] — Work on `main` only (trunk-based)
4. [[04-DECISIONS/decisions#Decision 4]] — Score formula exclusively in `packages/scoring/`
5. [[04-DECISIONS/decisions#Decision 5]] — Omnix at `.omnix/`

---

## 🔗 Cluster Connections

This note connects to:
- [[_INDEX]] — vault root
- [[MASTER_PLAN]] — mission + roadmap
- [[api-index]] — endpoint contracts
- [[scoring-knowledge]] — the formula
- [[intel-index]] — compute layer
- [[05-ARCHITECTURE/README]] — system diagram
- [[05-ARCHITECTURE/layered-modules]] — refactor map
- [[05-ARCHITECTURE/frontend-ux]] — UI design
- [[04-DECISIONS/decisions]] — why it's built this way
- [[06-WORKFLOWS/README]] — how to add to it

---

*Related: [[_INDEX]] · [[MASTER_PLAN]] · [[api-index]] · [[scoring-knowledge]] · [[intel-index]] · [[errors-index]] · [[05-ARCHITECTURE/README]] · [[05-ARCHITECTURE/layered-modules]] · [[04-DECISIONS/decisions]]*
