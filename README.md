# CareerOS Campus AI

> **Student-first, Intel-optimized placement-readiness loop for Indian colleges.**
> Resume + JD/job in -> ATS-safe + JD-matched + proof-linked output -> deterministic agent-driven fixes + export.

[![Week 1 — Live](https://img.shields.io/badge/Week%201-Live-16a34a?style=flat-square)](.)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-0071c5?style=flat-square)](apps/web)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square)](services/core-api)
[![Intel OpenVINO](https://img.shields.io/badge/Intel-OpenVINO%20%2B%20sklearnex-0071c5?style=flat-square)](services/intel-bench)
[![License: Private](https://img.shields.io/badge/License-Private-red?style=flat-square)](.)

---

## What this is

CareerOS Campus AI is **not** a job board, LinkedIn scraper, or recruiter marketplace.
It is a student-first placement-readiness workflow that still preserves college/TPO scalability.

| Without CareerOS | With CareerOS |
|---|---|
| Student has no clear fix path from resume to job | Student gets one deterministic flow from job search to export |
| Students submit Canva templates that ATS systems cannot parse | ATS parse-safety flagged on upload |
| Generic AI rewrites that invent experience | Proof-linked rewrites — unsupported claims flagged, never inserted |
| No aggregate skill-gap data | Department-level missing-skills heatmap |

---

## The 3-minute demo (student-first)

```
1. Student uploads resume (or uses existing parsed resume)
2. Student searches jobs in Jobs Feed
3. Clicks "Run deterministic agent"
4. Agent executes: ATS parse-safety -> JD match -> scorecard -> proof-linked rewrite -> PDF queue
5. Unsupported claims are shown and refused (never inserted)
6. Export job is created and downloadable when complete
7. Intel benchmark card shows measured sklearnex uplift
```

---

## Repo layout

```
CareerOS/
├── apps/
│   └── web/                   # Next.js 14 — student + officer surfaces
├── packages/
│   ├── contracts/             # JSON Schema: Resume, JD, Scorecard, Rewrite
│   ├── scoring/               # PlacementReadinessScore formula (Week 2)
│   └── ts-types/              # TS types generated from contracts/schemas
├── services/
│   ├── core-api/              # FastAPI orchestrator — auth, resume, ATS, scoring, agent
│   ├── ats-engine/            # Rule-based ATS parse-safety scorer (port 8001)
│   ├── ai-rewriter/           # Proof-linked rewriter — JSON schema output (port 8003)
│   ├── resume-parser/         # pdfplumber + python-docx + section extractor (port 8004)
│   ├── match-engine/          # TF-IDF + embeddings + sklearnex (Week 2)
│   ├── jobs-feed/             # Real-time jobs API adapter + Redis cache + seed fallback (port 8006)
│   └── intel-bench/           # OpenVINO + sklearnex benchmark harness (Week 5)
├── infra/                     # Docker and environment config
├── platform/
│   └── omnix/                 # Omnix runtime configuration
├── docs/
│   ├── adr/                   # Architecture Decision Records
│   └── research/              # Competitive landscape + monorepo structure research
├── tests/                     # Cross-domain e2e only
├── .claude/                   # Claude Code project config (rules, agents, MCP)
├── .cursor/                   # Cursor project config (agents, context, rules)
└── .obsidian-ai-memory/       # Engineering memory vault (sessions, errors, decisions)
```

---

## PlacementReadinessScore formula

Lives in `packages/scoring/` only — never duplicated in service code.

```
PlacementReadinessScore =
  0.35 × JD_Match
+ 0.20 × ATS_Parse_Safety
+ 0.20 × Evidence_Quality
+ 0.10 × Profile_Completeness
+ 0.10 × Interview_Readiness
+ 0.05 × Placement_Hygiene

JD_Match =
  0.35 × TFIDF_Cosine
+ 0.35 × Embedding_Cosine
+ 0.20 × Required_Skill_Recall
+ 0.10 × Eligibility_Rule_Score
```

Buckets: `0–49` high-risk · `50–69` borderline · `70–84` ready · `85–100` strong

---

## 5-week build plan

| Week | Deliverable | Status |
|---|---|---|
| **1** | Alembic schema + role auth + resume parser + enterprise frontend | ✅ Done |
| **2** | JD parser + match-engine (TF-IDF + embeddings + sklearnex) + score UI | 🔨 Next |
| **3** | AI rewriter (proof-linked, no fabrication) + before/after UI + PDF export | Planned |
| **4** | Officer dashboard — cohort heatmap, batch upload, review queue | Planned |
| **5** | Intel benchmark panel + pitch deck + 3-min demo script | Planned |

---

## Quick start

### Prerequisites

| Tool | Version |
|---|---|
| Node | 18+ |
| pnpm | 9+ |
| Python | 3.10+ |
| Docker + Compose | latest |

### Run the full stack

```bash
pnpm install                    # install JS deps
docker compose up -d --build    # start all backend services + databases
pnpm dev                        # start Next.js dev server
```

| URL | Service |
|---|---|
| `http://localhost:3000` | Web app |
| `http://localhost:8000/docs` | Core API — FastAPI docs |
| `http://localhost:8001/docs` | ATS Engine |
| `http://localhost:8004/docs` | Resume Parser |
| `http://localhost:8006/docs` | Jobs Feed |

```bash
docker compose down             # stop all services
```

### Database migrations (manual)

Docker Compose uses `AUTO_CREATE_TABLES=true` for local dev.
For a clean production-style migration:

```bash
cd services/core-api
alembic upgrade head
```

---

## Key conventions

- All HTTP via `apps/web/lib/api.ts` — never `fetch()` inline in components
- FastAPI route handlers stay slim — logic in `services/<svc>/app/services/`
- SQLAlchemy 2.0 mapped-column — `Mapped[T]` / `mapped_column(...)`, no `Column()`
- Schema change = Alembic migration file — never `entities.py` alone
- No Tailwind — CSS variables in `apps/web/app/globals.css`
- No fabrication — `services/ai-rewriter` flags unsupported claims, never invents them
- Score formula lives in `packages/scoring/` — never inlined in service code

### AI tool handoff

Every AI tool reads `.obsidian-ai-memory/` at session start. After meaningful work:

```bash
git add .obsidian-ai-memory/
git commit -m "memory: YYYY-MM-DD session digest"
git push
```

---

## Deterministic agent flow

- `POST /agent/run` -> runs ATS + match + score + rewrite + export queue
- `GET /agent/runs/{id}` -> step-wise status (`INIT -> ... -> DONE`)
- All steps persist in `agent_runs.summary_json` for recovery and audit

## Intel integration

| Workload | Baseline | Intel path | Conservative target |
|---|---|---|---|
| Embedding inference | PyTorch CPU | OpenVINO FP16 | 1.5×–4× throughput |
| TF-IDF + cosine | stock sklearn | sklearnex | 1.5×–8× speedup |
| KMeans cohort clustering | stock sklearn | sklearnex | 2×–8× speedup |

Benchmarks run at three sizes: 500 / 5 000 / 20 000 resumes.
Real measured numbers only — no vendor headline claims.

---

## Docs

- `docs/adr/` — Architecture Decision Records (why we pivoted, why this repo layout)
- `docs/research/` — Competitive landscape analysis + monorepo structure evidence
- `.obsidian-ai-memory/02-PROJECTS/bootcamp-brief.md` — Full Intel bootcamp context, demo script, judge Q&A

---

## License

Private. Not licensed for external use.
