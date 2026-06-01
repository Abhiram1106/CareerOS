# CareerOS — Teammate Handoff

**What this is:** A unified career intelligence platform for Indian students and freshers.
Resume builder + ATS scoring engine + job intelligence + proof-linked rewrites — all from one persistent career profile.

**The problem it solves:** 75–88% of Indian student resumes are rejected by ATS software before a human reads them. Students have no idea why, and no tool built for them fixes it.

**Product doc:** `CareerOS_Complete_Documentation.md` at repo root — read this first for full context.

---

## Get running in 10 minutes

```bash
git clone <repo-url>
cd CareerOS
docker compose up -d --build          # builds 7 images, starts 9 containers
cd apps/web && pnpm install && pnpm dev   # frontend on :3000
```

API docs: http://localhost:8000/docs
App: http://localhost:3000

---

## What's done vs what's next

| Status | What |
|---|---|
| ✅ Done | Auth, resume parse+score+export, JD matching, proof-linked rewrite, job search, structured profile CRUD, CI |
| 🔴 Next | Profile editor UI, resume builder (3 templates), multi-vendor ATS simulation |
| 🟡 Later | Application tracker UI, score history charts, guided AI wizard, B2B officer portal |

Full task breakdown: [10-whats-next.md](10-whats-next.md)

---

## Document index

| File | Read when |
|---|---|
| [01-architecture.md](01-architecture.md) | Understanding the system — services, ports, data flow |
| [02-dev-setup.md](02-dev-setup.md) | Setting up locally from scratch |
| [03-codebase-guide.md](03-codebase-guide.md) | Navigating the codebase, conventions, patterns |
| [04-api-reference.md](04-api-reference.md) | Working on backend endpoints or frontend API calls |
| [05-scoring-system.md](05-scoring-system.md) | Touching anything in `packages/scoring/` or `match-engine` |
| [06-frontend-guide.md](06-frontend-guide.md) | Working on `apps/web/` |
| [07-database-schema.md](07-database-schema.md) | Schema changes, migrations, new entities |
| [08-ai-ml-stack.md](08-ai-ml-stack.md) | Embeddings, rewriter, ATS engine, Intel layer |
| [09-testing-and-ci.md](09-testing-and-ci.md) | Running tests, CI jobs, adding test cases |
| [10-whats-next.md](10-whats-next.md) | Picking up the next task |

---

## Key people / ownership

| Area | Owner |
|---|---|
| Sole contributor to date | Abhiram Jonnadula |
| Teammates joining now | — (you) |

---

## Quick orientation

```
CareerOS/
├── apps/web/              Next.js 14 frontend (TypeScript strict)
├── services/
│   ├── core-api/          FastAPI — auth, profile, resume, scoring, jobs
│   ├── resume-parser/     PDF/DOCX → structured sections
│   ├── match-engine/      TF-IDF + MiniLM embeddings + skill matching
│   ├── ats-engine/        ATS parse-safety analyzer
│   ├── ai-rewriter/       Proof-linked rule-based rewriter
│   └── jobs-feed/         Adzuna API + seed job data
├── packages/
│   └── scoring/           PlacementReadinessScore formula (single source of truth)
├── tests/golden/          Discrimination gate + test corpus
├── docs/
│   ├── handoff/           ← you are here
│   └── benchmarks/        Intel performance measurements
└── docker-compose.yml     Starts everything
```
