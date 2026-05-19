# .claude/CLAUDE.md — Claude Code project config

> Auto-loaded by Claude Code. Project-shared (committed). Personal overrides
> go in `.claude/CLAUDE.local.md` (gitignored).
>
> For project positioning, stack, and completion gate, see the root
> `CLAUDE.md` and `AGENTS.md`. This file holds Claude-Code-specific bits
> only.

## Modular rules

Claude Code loads `.claude/rules/*.md` matching the active file scope:

| Rule file | Scope |
|---|---|
| `rules/code-style.md` | All code edits |
| `rules/frontend/react.md` | `apps/web/**/*.{ts,tsx}` |

Add new rule files under `rules/<scope>/` and document them here.

## Subagents + skills

| Folder | Status |
|---|---|
| `agents/` | Empty — using global agents only |
| `skills/` | Empty — using global skills only |

Add project-specific subagents/skills when a task pattern is too
codebase-specific to belong in the global library.

## MCP

Project-scoped MCP servers live in `.claude/.mcp.json`. Currently empty.

## Permissions

`.claude/settings.json` is the committed permission baseline (team-shared).
`.claude/settings.local.json` (gitignored) holds your personal allow/deny
overrides.
