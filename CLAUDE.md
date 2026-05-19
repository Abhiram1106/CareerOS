# CLAUDE.md — CareerOS Campus AI

> Claude Code auto-loads this file on every session. It defers to `AGENTS.md`
> for the Omnix startup protocol and to `.claude/CLAUDE.md` for project
> Claude-specific config.

@AGENTS.md

## Project at a glance

- **Name**: CareerOS Campus AI
- **Positioning**: Intel-optimized placement-readiness operating layer for Indian colleges
- **Stack**: Next.js 14 (`apps/web`) · FastAPI (`services/core-api`, `services/ats-engine`, `services/ai-rewriter`) · PostgreSQL · Redis · Celery · WeasyPrint
- **Monorepo layout**: `apps/` · `packages/` · `services/` · `infra/` · `platform/` · `docs/` · `tests/`
- **Plan**: `C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md`
- **ADRs**: `docs/adr/`

## Project Claude config

See `.claude/CLAUDE.md` for Claude Code-specific instructions, modular rules
(`code-style.md`, `frontend/react.md`), and the project MCP config.

## Memory retrieval mode

`balanced` by default. Switch to `deep` for architecture changes, `debugging`
for error investigation, `minimal` for one-liner answers.

## Completion gate

Don't say "done" until:

- [ ] Changed files are correct and match intent
- [ ] Tests/typecheck ran (state result or reason skipped)
- [ ] Docs updated if behavior changed
- [ ] Session digest written (skip only for read-only sessions)
- [ ] Error memory updated if a bug was fixed
- [ ] No secrets in any written file
- [ ] Open risks listed if any remain
