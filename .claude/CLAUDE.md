# .claude/CLAUDE.md — Claude Code project config

> Auto-loaded by Claude Code on every session. Project-shared and committed.
> Personal overrides go in `.claude/CLAUDE.local.md` (gitignored).
>
> Project positioning, stack, and completion gate: see root `CLAUDE.md` and `AGENTS.md`.
> This file holds Claude Code-specific config only.

## Modular rules

| Rule file | Activates on |
|---|---|
| `.claude/rules/code-style.md` | All code edits in the repo |
| `.claude/rules/frontend/react.md` | `apps/web/**/*.{ts,tsx}` |

Rules are tailored to this exact stack (Next.js 14 app router, FastAPI, SQLAlchemy 2.0,
Pydantic v2, `useCareerOSWorkspace` hook pattern, CSS variables dark theme).
No Tailwind, no shadcn, no Radix — do not apply generic React rules.

## Subagents and skills

| Folder | Status | Notes |
|---|---|---|
| `agents/` | Empty | Using global Claude agents only |
| `skills/` | Empty | Using global skills only |

Add a project-specific agent or skill when a task pattern is too codebase-specific
for the global library (e.g. "validate a PlacementReadinessScore change against
`packages/scoring/` test fixtures").

## MCP servers

`.claude/.mcp.json` — project-scoped MCP. Empty. Add servers (postgres, github)
here when the project needs them. Never commit real credentials.

## Permissions

`.claude/settings.json` — committed team baseline.
`.claude/settings.local.json` — personal allow/deny overrides (gitignored).

## Key project paths (for quick navigation)

| What | Where |
|---|---|
| Core API routes | `services/core-api/app/main.py` |
| DB models | `services/core-api/app/models/entities.py` |
| Alembic migrations | `services/core-api/migrations/versions/` |
| Service clients (httpx) | `services/core-api/app/services/clients.py` |
| Auth + dependencies | `services/core-api/app/services/auth.py`, `app/dependencies.py` |
| ATS scorer | `services/ats-engine/app/main.py` |
| AI rewriter | `services/ai-rewriter/app/main.py` |
| Score formula | `packages/scoring/` (pending Week 2) |
| JSON contracts | `packages/contracts/schemas/` |
| Web panes | `apps/web/components/panes/` |
| UI primitives | `apps/web/components/ui/primitives.tsx` |
| API client | `apps/web/lib/api.ts` |
| State hook | `apps/web/hooks/useCareerOSWorkspace.ts` |
| CSS variables | `apps/web/app/globals.css` |
| Omnix memory | `.obsidian-ai-memory/02-PROJECTS/` |
| Error memory | `.obsidian-ai-memory/03-ERRORS/error-memory.md` |
| Decisions log | `.obsidian-ai-memory/04-DECISIONS/decisions.md` |
| Plan file | `C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md` |
