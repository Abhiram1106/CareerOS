# Session — Pivot, restructure, monorepo scaffold

**Date**: 2026-05-19
**Tool**: Claude Code (Opus 4.7)
**Duration**: long — full restructure + Phase 2 scaffold
**Status**: Phase 1 + Phase 2 complete; Week 1 step 3 (Alembic delta + parser) next

---

## Goal

Take CareerOS — a broad polished MVP (Next.js dark UI, FastAPI core-api +
ats-engine + ai-inference + NEXUS ATS monolith, Stripe/Razorpay billing, 15
hardcoded job listings) — and pivot it into **CareerOS Campus AI**, an Intel-
optimized placement-readiness operating layer for Indian colleges.

Two research documents drove the pivot:
- `deep-research-report.md` — competitive landscape + scoring formula + MVP plan
- `deep-research-report (1).md` — monorepo structure evidence

User also requested the project-level `.claude/` layout per the screenshot:
`settings.json` + `settings.local.json` (gitignored) + `CLAUDE.md` +
`CLAUDE.local.md` (gitignored) + `agents/` + `skills/` + `rules/` + `.mcp.json`.

---

## What landed

### Phase 1 (commits c327416 + 172160a)

**Cut on `main`** (preserved on `origin/archive/pre-campus-ai`):
- NEXUS ATS monolith + blueprints + scratch dirs (`backend/ATS/`)
- Legacy v0 monolith (`backend/legacy/`)
- Public job board service (`backend/platform/services/job-intel/`)
- Billing surface: `payment.py`, all `/billing/*` routes, Stripe + Razorpay deps, Subscription + PaymentTransaction models
- Alerts surface: `/jobs/alerts/*` routes, JobAlert + AlertNotification models, dispatch_job_alerts task + beat schedule
- Application tracker: `/applications/*` routes, ApplicationTrack model
- Frontend cuts: BillingPane, NexusPane, Nexus*Card, JobAlertsCard, DashboardApplicationsCard
- Test artefacts: `*.db` files, `.tmp_docx_extract2/`, generated PDFs

**Restructured**:
- `frontend/` → `apps/web/`
- `backend/platform/services/{core-api,ats-engine,ai-inference}` → `services/{core-api,ats-engine,ai-rewriter}` (ai-inference renamed per its new purpose)
- `backend/docs/` → `docs/legacy/v0-careeros-docs/`
- `docker-compose.yml` + `.env.example` promoted to repo root
- Added `pnpm-workspace.yaml` + root `package.json`

**Stripped**:
- `services/core-api/app/main.py`: 851 → 270 lines, 73 → 15 routes
- `entities.py`, `clients.py`, `schemas/contracts.py`, `workers/tasks.py`, `workers/celery_app.py`, `config.py`, `requirements.txt`
- `apps/web/lib/api.ts`: 123 → 64 lines
- `apps/web/hooks/useCareerOSWorkspace.ts`: 530 → 212 lines
- `apps/web/app/page.tsx`: 132 → 73 lines
- `apps/web/components/panes/JobsPane.tsx`: rewritten as placeholder readiness dashboard

**Verified**: `npx tsc --noEmit` clean on `apps/web`; all `services/*` Python files AST-parse clean.

### Phase 2 (this commit, in progress)

**Monorepo skeleton** per `deep-research-report (1).md` small-team variant + Omnix integration in `platform/`:

```
apps/web/                         (existing — Next.js 14)
packages/                         (NEW: README + sub-READMEs)
  ├── contracts/{openapi,schemas}/
  ├── scoring/
  ├── ts-types/
  ├── frontend/  (reserved)
  └── backend/   (reserved)
services/{core-api,ats-engine,ai-rewriter}/   (existing)
infra/{docker,environments}/      (NEW: README)
platform/                          (NEW: ci, scripts, build, omnix — each with README)
docs/                              (NEW: adr/{0001-pivot, 0002-monorepo}, README)
tests/                             (NEW: README placeholder for cross-domain e2e)
```

**Project Claude config** at `.claude/`:
- `CLAUDE.md` (committed) — Claude-specific config, defers to root for project context
- `CLAUDE.local.md.example` — template; `.local.md` itself is gitignored
- `settings.json` (committed) + `settings.local.json` (gitignored)
- `agents/README.md`, `skills/README.md` — placeholders for future project-specific subagents/skills
- `rules/code-style.md` + `rules/frontend/react.md` — modular rule files referenced from `.claude/CLAUDE.md`
- `.mcp.json` — project-scoped MCP server config (empty)

**Root protocol docs reconciled**:
- Root `CLAUDE.md` rewritten as Campus AI project context + `@AGENTS.md` include
- `.claude/CLAUDE.md` trimmed to Claude-Code-specific bits only (no duplication)
- `AGENTS.md` retained as Omnix startup protocol source of truth

**Other**:
- `CODEOWNERS` at repo root mapping every top-level dir to `@Abhiram1106` (pattern in place for future collaborators)
- Top-level `README.md` written — Campus AI positioning, repo layout, quick start, contribution guide
- `.gitignore` reconciled: track team-shared AI config (`.claude/CLAUDE.md`, `.cursor/rules/`, `.omnix/{agents,workflows,commands,settings}`, full `.obsidian-ai-memory/` vault), ignore personal overrides (`.claude/{settings.local.json,CLAUDE.local.md}`) and runtime caches (`.omnix/{memory,cache}/`)

**Omnix memory vault populated**:
- `02-PROJECTS/{project-context, active-goals, current-state, vault-index}.md` — filled in (previously `(fill in)` placeholders)
- `03-ERRORS/{error-memory, anti-patterns}.md` — populated with this session's incident (git mv + edit + commit losing edits) and prevention rules
- `04-DECISIONS/decisions.md` — created, indexes the five active decisions referenced in ADRs
- `01-SESSIONS/2026-05-19/session-restructure.md` — this file

---

## Decisions made (linked from `04-DECISIONS/decisions.md`)

1. **Pivot to Campus AI** — ADR 0001
2. **Hybrid small-team monorepo with Omnix in platform/** — ADR 0002
3. **Work on `main` only, no feature branches** — recoverable via archive branch
4. **Score formula source of truth: `packages/scoring/`**
5. **Omnix runtime stays at `.omnix/`, `platform/omnix/` is the documented target for the future migration**

---

## Errors fixed

- **`git mv` + post-rename edit + commit lost the edits** — fix: always
  `git add -u` before `git commit` after editing renamed files. Promoted
  to `anti-patterns.md`.

---

## Open risks (for `current-state.md` → "what's blocked")

- PDF parsing fragility on Indian fresher resumes (Canva, two-column,
  scanned). Mitigation: checked-in fixture corpus.
- OpenVINO INT8 accuracy delta unknown until Week 5 benchmarks.
  Mitigation: fall back to FP16 if needed.
- No real pilot data in 5 weeks. Mitigation: synthetic + hand-labeled
  cohort for demo; outcome lift framed as next step in pitch.

---

## Next session

Week 1 step 3:
1. Real Alembic delta migration: add colleges, departments,
   resume_sections, resume_evidence, job_descriptions, scorecards,
   recommendations, batches, batch_resumes, events_audit, benchmark_runs.
2. Add `role` claim to JWT and gate routes.
3. Implement `services/resume-parser` (pdfplumber + python-docx + section
   extractor) with checked-in fixture corpus.
4. Wire `apps/web/(student)/resume/` to call the parser and render
   structured sections.

---

## Stats

- **Tracked files**: 71 (pre-pivot was 131)
- **Commits this session on `main`**: 2 so far (c327416, 172160a); Phase 2 commit pending
- **Lines net**: −6452 +960 across Phase 1
- **Verification**: `tsc --noEmit` clean; all Python AST-parses clean
