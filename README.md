# CareerOS Campus AI

> **Intel-optimized placement-readiness operating layer for Indian colleges.**
> Resumes in → ATS-safe + JD-matched + proof-linked scoring out →
> student fixes + officer cohort dashboard → measured Intel benchmarks.

[![Week 1 — Live](https://img.shields.io/badge/Week%201-Live-16a34a?style=flat-square)](.)
[![TypeScript](https://img.shields.io/badge/TypeScript-strict-0071c5?style=flat-square)](apps/web)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square)](services/core-api)
[![Intel OpenVINO](https://img.shields.io/badge/Intel-OpenVINO%20%2B%20sklearnex-0071c5?style=flat-square)](services/intel-bench)
[![License: Private](https://img.shields.io/badge/License-Private-red?style=flat-square)](.)

---

## What this is

CareerOS Campus AI is **not** a resume builder, job board, or LinkedIn scraper.
It is a campus placement workflow system — the difference is the placement officer.

| Without CareerOS | With CareerOS |
|---|---|
| Officer discovers bad resumes after companies reject students | Officer sees cohort readiness before the drive |
| Students submit Canva templates that ATS systems cannot parse | ATS parse-safety flagged on upload |
| Generic AI rewrites that invent experience | Proof-linked rewrites — unsupported claims are flagged, never inserted |
| No aggregate skill-gap data | Department-level missing-skills heatmap |

The full research case is in `deep-research-report.md`. The product architecture is in `docs/adr/`.

---

## The demo loop (3 minutes)

```
1. Placement officer pastes a company JD (e.g. TCS Ninja, Accenture ASE)
2. Uploads 20 student resumes as a batch
3. Dashboard: readiness buckets, department breakdown, top missing skills
4. Opens one low-scoring student — ATS risks highlighted, score breakdown shown
5. Clicks "Rewrite with verified evidence" — one unsupported claim refused, others improved
6. Score lifts 48 → 73
7. Intel panel: p50/p95 latency + throughput for baseline vs OpenVINO/sklearnex path
```

---

## Monorepo layout

```
CareerOS/
├── apps/
│   └── web/                        # Next.js 14 — student surface + (future) officer surface
├── packages/
│   ├── contracts/                  # JSON Schema: Resume, JD, Scorecard, Rewrite
│   ├── scoring/                    # Python: PlacementReadinessScore formula (Week 2)
│   ├── ts-types/                   # TypeScript types generated from contracts/schemas
│   ├── frontend/                   # (reserved) shared React components
│   └── backend/                    # (reserved) shared Python utils
├── services/
│   ├── core-api/                   # FastAPI orchestrator — auth, resume, ATS, scoring
│   ├── ats-engine/                 # Rule-based ATS parse-safety scorer (port 8001)
│   ├── ai-rewriter/                # Proof-linked rewriter — JSON schema output (port 8003)
│   ├── resume-parser/              # pdfplumber + python-docx + section extractor (port 8004)
│   ├── match-engine/               # TF-IDF + embeddings + sklearnex (Week 2, port 8005)
│   └── intel-bench/                # OpenVINO + sklearnex benchmark harness (Week 5)
├── infra/                          # Docker, environment overrides
├── platform/                       # CI, scripts, build presets, Omnix config
├── docs/
│   ├── adr/                        # Architecture Decision Records (ADR 0001, 0002)
│   ├── architecture/               # System diagrams, data flows
│   ├── pitch/                      # 6-slide deck + 3-min demo script (Week 5)
│   └── benchmarks/                 # Intel measurement methodology + raw runs
├── tests/                          # Cross-domain e2e only
├── .claude/                        # Claude Code project config
├── .cursor/                        # Cursor project config (agents, context, rules)
└── .obsidian-ai-memory/            # Omnix engineering memory vault (sessions, errors, decisions)
```

---

## PlacementReadinessScore formula

The scoring formula lives in `packages/scoring/` only — never duplicated in service code.

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
| **1** | Alembic migration + role auth + resume upload + PDF/DOCX parser | ✅ Done |
| **2** | JD parser + `services/match-engine` (TF-IDF + embeddings) + score breakdown UI | 🔨 Next |
| **3** | `services/ai-rewriter` retarget — proof-linked JSON schema + before/after diff UI | Planned |
| **4** | Officer dashboard route group — cohort heatmap, batch upload, review queue | Planned |
| **5** | `services/intel-bench` — OpenVINO + sklearnex benchmarks + pitch deck + demo script | Planned |

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
# 1. Install JS dependencies
pnpm install

# 2. Start all backend services + databases
docker compose up -d --build

# 3. Start the Next.js dev server
pnpm dev
```

| URL | Service |
|---|---|
| http://localhost:3000 | Web app (student workspace + hero) |
| http://localhost:8000/docs | Core API — FastAPI interactive docs |
| http://localhost:8001/docs | ATS Engine |
| http://localhost:8004/docs | Resume Parser |

Stop services:
```bash
docker compose down
```

### Run only the web app (no Docker)

```bash
pnpm install
pnpm dev
```
The app still works — auth and upload endpoints require the backend, but the hero page and UI are fully browsable.

### Database migrations

Docker Compose uses `AUTO_CREATE_TABLES=true` for local dev convenience.
For production or manual migration:
```bash
cd services/core-api
alembic upgrade head
```

---

## Development conventions

All conventions are enforced by `.claude/rules/` and `.cursor/rules/`.
See `AGENTS.md` for the Omnix startup protocol every AI tool follows.

Key rules:
- **All HTTP in `apps/web/lib/api.ts`** — never `fetch()` inline from components
- **FastAPI route handlers stay slim** — logic in `services/<svc>/app/services/`
- **SQLAlchemy 2.0** — `Mapped[T]` / `mapped_column(...)`, no `Column()`
- **Schema change = Alembic migration** — never rely on `entities.py` alone
- **No Tailwind** — CSS variables in `apps/web/app/globals.css`
- **No fabrication** — `services/ai-rewriter` flags unsupported claims, never invents them
- **Score formula once** — `packages/scoring/`, never inline

### AI-tool cross-platform handoff

This repo uses Omnix for engineering memory. Any AI tool (Claude Code, Cursor, Copilot)
reads `.obsidian-ai-memory/` at session start and writes a digest after meaningful work:

```bash
# After a meaningful session:
git add .obsidian-ai-memory/
git commit -m "memory: YYYY-MM-DD session digest"
git push
```

---

## Intel integration

| Workload | Baseline | Intel path | Target |
|---|---|---|---|
| Embedding inference | PyTorch CPU | OpenVINO FP16 | 1.5×–4× throughput |
| TF-IDF + cosine similarity | stock sklearn | sklearnex patch | 1.5×–8× speedup |
| KMeans cohort clustering | stock sklearn | sklearnex | 2×–8× speedup |
| Full score pipeline | mixed | selectively accelerated | 20–80% improvement |

Benchmarks are real measurements at three dataset sizes (500 / 5 000 / 20 000 resumes).
No vendor headline numbers. Accuracy delta is measured before committing any quantisation.

---

## Research and decisions

- `deep-research-report.md` — competitive landscape, scoring formula, MVP plan, guardrails
- `deep-research-report (1).md` — monorepo structure evidence (hybrid variant selected)
- `docs/adr/0001-pivot-to-campus-ai.md` — why we repositioned
- `docs/adr/0002-monorepo-structure.md` — why this repo layout
- `C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md` — full plan

---

## License

Private. Not licensed for external use.
