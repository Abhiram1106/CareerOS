---
tags: [hub, mission, roadmap, bootcamp, moc]
type: hub
created: 2026-05-21
updated: 2026-05-21
links: [_INDEX, scoring-knowledge, intel-index, architecture-index, session-index]
---

# 🎯 MASTER_PLAN — CareerOS Campus AI

> **Mission:** Ship a 9+/10 Intel AI Bootcamp submission in 5 weeks.  
> Single sharp positioning: *"The placement-readiness operating layer for Indian colleges."*

← [[_INDEX]] | [[architecture-index]] → | [[scoring-knowledge]] →

---

## 🏆 The Problem We Solve

> 42.6% of Indian graduates are not employable (Mercer Mettl 2025).  
> Every college has a TPO. None have a system. We build the system.

| Pain | Today | CareerOS |
|------|-------|----------|
| Resume review | WhatsApp + Excel | Batch upload → AI parse → scored |
| Company matching | Manual | JD paste → hybrid TF-IDF + embeddings |
| Cohort intel | Zero visibility | Dept heatmaps, skill gaps, readiness % |
| AI trust | Black boxes | Proof-linked rewrites, evidence IDs |
| Compute story | Generic cloud | Intel OpenVINO + sklearnex, measured |

**Not:** a job board · a LinkedIn scraper · a resume builder · a recruiter marketplace.

---

## 📅 5-Week Roadmap

```
Week 1 ✅  Foundation
Week 2 🔨  Intelligence (CURRENT)
Week 3 ⏳  Rewriter
Week 4 ⏳  Officer Surface
Week 5 ⏳  Intel Bench + Pitch
```

### Week 1 ✅ Foundation (done)

- [x] Phase 1: Archive NEXUS/billing/job-board legacy
- [x] Phase 2: Monorepo scaffold (`apps/`, `services/`, `packages/`)
- [x] W1.3: Alembic migration — 11 new tables (colleges, departments, scorecards, batches, etc.)
- [x] W1.4: Role-based auth — JWT + `require_student` / `require_officer` / `require_admin`
- [x] W1.5: Resume parser service — pdfplumber + python-docx + spaCy section extractor
- [x] Layered architecture — Phases 1–7 complete (main.py = health only)
- [x] Frontend auth — login/register split-panel, demo mode, RBAC routing

→ See [[session-index]] for full trail. Architecture at [[05-ARCHITECTURE/layered-modules]].

### Week 2 🔨 Intelligence (in progress)

- [ ] JD parser → `job_descriptions` table → `skills_json` + `eligibility_json`
- [ ] `services/match-engine/` — TF-IDF cosine + embedding cosine + sklearnex
- [ ] `packages/scoring/` — [[scoring-knowledge|PlacementReadinessScore]] formula (single source)
- [ ] Score breakdown UI → `/workspace` JD Match Scan tab wired to real API
- [ ] Alembic migration for `scorecards` + `job_descriptions` population

→ See [[02-PROJECTS/active-goals]] for checkboxes. Formula at [[scoring-knowledge]].

### Week 3 ⏳ AI Rewriter

- [ ] `services/ai-rewriter/` — proof-linked JSON schema rewriter
- [ ] Evidence IDs — every suggestion must have `evidence_ids[]` from resume JSON
- [ ] `unsupported_claims[]` — refused, never in `section_rewrites[]`
- [ ] Before/after diff UI in workspace
- [ ] WeasyPrint ATS-safe PDF export

→ Proof-linked design at [[api-index#Rewriter Contract]].

### Week 4 ⏳ Officer Surface

- [ ] `apps/web/app/(officer)/` route group
- [ ] Batch upload — multiple resumes vs one JD
- [ ] Department readiness heatmap
- [ ] Proof-linked review queue (approve / return with tag)
- [ ] Readiness PDF report export

→ Officer UI at [[05-ARCHITECTURE/frontend-ux#Officer Surface]].

### Week 5 ⏳ Intel Bench + Pitch

- [ ] `services/intel-bench/run.py` — real measurements (NOT vendor claims)
- [ ] `/lab/intel` panel — p50/p95 latency table, throughput chart
- [ ] 6-slide pitch deck
- [ ] 3-minute demo script rehearsed
- [ ] `benchmark_runs` table populated with real numbers

→ Full Intel story at [[intel-index]]. Demo script at [[02-PROJECTS/bootcamp-brief]].

---

## 🎬 3-Minute Demo Script

> **Scene 1 — Officer dashboard** (start here, not login)  
> "Today we have an Accenture ASE drive. I paste the JD."

> **Scene 2 — Batch upload**  
> "20 CSE resumes uploaded in one click."

> **Scene 3 — Intel processing** (show spinner with Intel badge)  
> "Intel-accelerated TF-IDF + embedding pipeline scores each resume."

> **Scene 4 — Dashboard result**  
> `20 scanned · 6 ready · 9 borderline · 5 high-risk · top gap: SQL · avg: 62%`

> **Scene 5 — Student fix**  
> Score: 48 → High Risk. ATS issue detected. Click "Rewrite."  
> One unsupported claim REFUSED. Two bullets improved. Score: 48 → 73.

> **Scene 6 — Intel panel**  
> Baseline vs OpenVINO+sklearnex. p50 latency table. accuracy_delta < 0.5%.

→ Details at [[02-PROJECTS/bootcamp-brief]] · Intel numbers at [[intel-index#Benchmark Targets]].

---

## 📊 Scoring Target: 9+/10

| Judge Criterion | Why We Score High |
|----------------|------------------|
| Problem severity | 42.6% unemployability, 8.47L engineers/year |
| Demo potential | Upload → score → rewrite → dashboard → benchmark |
| Intel relevance | CPU-bound NLP workloads, real measured speedups |
| Technical depth | 6-service monorepo, Alembic, Pydantic v2, Celery |
| Social impact | Directly fixes TPO workflow at India's 4.33cr enrolments |
| Business potential | B2B SaaS to TPO offices, institutional sticky buyer |
| Pitch clarity | One sharp positioning, not "AI resume builder" |

---

## 🚫 What This Is NOT

- ~~Not a job board~~ → See [[04-DECISIONS/decisions#Decision 1 — Pivot]]
- ~~Not a LinkedIn scraper~~ → API terms restrict this
- ~~Not a recruiter marketplace~~ → NEXUS ATS archived
- ~~Not a billing product~~ → Cut in Week 1 restructure
- ~~Not a mobile app~~ → Web-only MVP

---

## 👥 Three Personas

**Priya** (student, CSE final year) → uses `/workspace` → uploads resume → sees score → applies rewrite  
**Mr. Ramesh** (TPO) → uses `/officer` → batch upload → cohort dashboard → approves rewrites  
**Dr. Mehta** (college admin) → monthly report → placement PDF → department comparison

---

*Related: [[_INDEX]] · [[scoring-knowledge]] · [[intel-index]] · [[architecture-index]] · [[session-index]] · [[02-PROJECTS/bootcamp-brief]] · [[02-PROJECTS/active-goals]]*
