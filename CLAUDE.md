# CLAUDE.md — CareerOS Campus AI

> Claude Code auto-loads this file every session.
> Full protocol and rules → `AGENTS.md` (read first) and `.claude/CLAUDE.md`.

@AGENTS.md

## Project at a glance

- **Name**: CareerOS Campus AI — Intel AI Bootcamp submission
- **Positioning**: Intel-optimized placement-readiness operating layer for Indian colleges
- **Stack**: Next.js 14 (`apps/web`) · FastAPI (`services/`) · PostgreSQL · Redis · Celery · WeasyPrint
- **Layout**: `apps/` · `packages/` · `services/` · `infra/` · `platform/` · `docs/` · `tests/`
- **ADRs**: `docs/adr/`
- **Research**: `docs/research/`
- **Bootcamp brief**: `.obsidian-ai-memory/02-PROJECTS/bootcamp-brief.md`

## Claude Code config

Rules and path quick-nav → `.claude/CLAUDE.md`

## Completion gate

Don't say "done" until:

- [ ] Changed files correct and match intent
- [ ] `tsc --noEmit` clean (state result or reason skipped)
- [ ] Python AST-parse clean on all touched services
- [ ] Session digest written (skip only for read-only sessions)
- [ ] Error memory updated if a bug was fixed
- [ ] No secrets in any written file
- [ ] Open risks listed if any remain
