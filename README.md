# CareerOS Campus AI

> Intel-optimized **placement-readiness operating layer** for Indian colleges.
> Resumes in → ATS-safe + JD-matched + proof-linked scoring out → student
> fixes + placement-officer cohort dashboard out → Intel benchmarks proving
> the inference/analytics path is real, not decoration.

**Status**: post-pivot restructure complete. Feature build (Weeks 1–5)
starts next. See `docs/adr/0001-pivot-to-campus-ai.md`.

---

## Why this exists

Indian colleges push thousands of students into placement drives every year,
but employability remains weak: Mercer | Mettl's 2025 Graduate Skill Index
puts overall fresher employability at **42.6%**. The placement office
discovers resume-format problems and JD-mismatch gaps *after* companies
reject students. CareerOS Campus AI flips that: parse every resume in the
cohort, compare against the actual JD, score it on six dimensions, give
students AI-guided fixes that **refuse to fabricate**, and give the
placement officer a live readiness dashboard.

**The Intel angle is honest.** Sentence-transformer inference runs through
OpenVINO; TF-IDF + cosine + KMeans cohort clustering runs through Intel
Extension for Scikit-learn. Benchmarks are real measurements on real
workloads, not vendor slideware.

For the full pitch and demo script, see `docs/pitch/` (Week 5 deliverable).

---

## Repo layout

```
.
├── apps/                  # Deployable applications
│   └── web/               # Next.js 14 — student + (future) officer surface
├── packages/              # Reusable libraries (no deployables here)
│   ├── contracts/         # Cross-language JSON schemas + OpenAPI specs
│   ├── scoring/           # Python: PlacementReadinessScore formula
│   ├── ts-types/          # TS types generated from contracts/schemas
│   ├── frontend/          # (reserved) shared React + design tokens
│   └── backend/           # (reserved) shared Python utils
├── services/              # Backend microservices
│   ├── core-api/          # FastAPI orchestrator: auth, profile, resume, ATS, scoring
│   ├── ats-engine/        # Rule-based ATS-parse-safety scorer
│   └── ai-rewriter/       # Proof-linked AI rewriter (formerly ai-inference)
├── infra/                 # IaC (docker, environments)
├── platform/              # Engineering platform: ci/, scripts/, build/, omnix/
├── docs/                  # ADRs, architecture, pitch, benchmarks, legacy
├── tests/                 # Cross-domain end-to-end tests only
├── .claude/               # Project Claude Code config (rules, agents, skills, MCP)
├── .cursor/rules/         # Project Cursor rules
├── .omnix/                # Omnix Runtime (committed config + gitignored cache)
└── .obsidian-ai-memory/   # Long-term engineering memory vault (Omnix)
```

See `docs/adr/0002-monorepo-structure.md` for the rationale (hybrid small-team
variant with Omnix integration baked into `platform/`).

---

## Quick start

### Prerequisites
- Node 18+ and pnpm 9+
- Python 3.10+
- Docker + Docker Compose
- PostgreSQL 16 (via Docker)
- Redis 7 (via Docker)

### Bring up the stack
```bash
pnpm install
docker compose up -d --build
pnpm dev
```

Services exposed:
- **Web app**: http://localhost:3000
- **Core API docs**: http://localhost:8000/docs

Other services (`ats-engine`, `ai-rewriter`) are internal-only.

Stop the Docker services when you are done:
```bash
docker compose down
```

### Web app (dev)
```bash
pnpm install
pnpm dev
```

### Workspace-level commands
```bash
pnpm dev        # alias: pnpm --filter web dev
pnpm build      # alias: pnpm --filter web build
pnpm web <cmd>  # any script in apps/web
```

### Database migrations
Docker Compose is configured for local development and auto-creates the current
schema. If you run `services/core-api` outside Docker with
`AUTO_CREATE_TABLES=false`, run migrations manually:

```bash
cd services/core-api
alembic upgrade head
```

---

## How to contribute

1. Read `AGENTS.md` (Omnix startup protocol — applies to humans and AI tools alike).
2. Check `.obsidian-ai-memory/02-PROJECTS/active-goals.md` for current priorities.
3. Check `.obsidian-ai-memory/03-ERRORS/error-memory.md` before debugging anything.
4. Follow the rules in `.claude/rules/` and `.cursor/rules/` for the code area you're touching.
5. Open a PR; CODEOWNERS will request the right reviewer.

### Plan + research

- **Plan file**: `C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md`
- **Strategy research**: `deep-research-report.md` (competitive landscape, scoring, MVP plan)
- **Structure research**: `deep-research-report (1).md` (monorepo evidence)
- **ADRs**: `docs/adr/`

---

## License

Private. Not licensed for external use yet.
