# PROJECT_CONTEXT.md — CareerOS Campus AI

> Quick-load stub for AI tools that read this file at startup.
> Full living context is in `.obsidian-ai-memory/02-PROJECTS/project-context.md`.

- **Project Name**: CareerOS Campus AI
- **Tagline**: Intel-optimized placement-readiness operating layer for Indian colleges
- **Stack**: Next.js 14 (apps/web) · FastAPI 0.115 (services/) · PostgreSQL 16 · Redis 7 · Celery · WeasyPrint
- **Package Manager**: pnpm 9 (JS workspaces) · pip per Python service
- **Project Type**: Polyglot monorepo — hybrid small-team variant (apps / packages / services / infra / platform / docs / tests)
- **Current Phase**: Week 1 — Alembic delta migration + role-based auth + resume upload + PDF/DOCX parser
- **Plan file**: `C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md`
- **ADRs**: `docs/adr/0001-pivot-to-campus-ai.md` · `docs/adr/0002-monorepo-structure.md`
- **Known Errors**: `.obsidian-ai-memory/03-ERRORS/error-memory.md`
- **Do Not Repeat**: `.obsidian-ai-memory/03-ERRORS/anti-patterns.md`
- **Next Steps**: see `.obsidian-ai-memory/02-PROJECTS/active-goals.md`

## What this project is NOT

- Not a public job board
- Not a LinkedIn scraper or importer
- Not a recruiter platform (NEXUS ATS cut — see archive branch)
- Not a billing/subscription product (Stripe/Razorpay cut)
- Not "just another resume builder"

## Core demo workflow (3 minutes)

1. Placement officer pastes company JD (e.g. TCS Ninja)
2. Uploads 20 student resumes as a batch
3. Dashboard shows readiness buckets (ready / borderline / high-risk), dept breakdown, top missing skills
4. Opens one low-scoring student — ATS risks highlighted, JD match breakdown shown
5. Clicks "Rewrite with verified evidence" — one unsupported claim is **refused**, others improved
6. Score lifts from e.g. 48 → 73
7. Intel panel shows p50/p95 latency + throughput for baseline vs OpenVINO/sklearnex path
