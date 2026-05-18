# AI_RULES.md

Universal engineering rules for every AI tool on this project.

## Source of truth

Full rules live in the omnix monorepo:
- `packages/core/standards/ai-collaboration.md`
- `packages/core/standards/self-orchestration.md`
- `packages/core/standards/context-engineering.md`

## Quick reference

| Rule | Summary |
|---|---|
| Memory first | Read Obsidian vault before every response |
| No repeat errors | Check `03-ERRORS/error-memory.md` before fixing |
| Small changes | One concern per edit |
| Verify before done | Run tests/lint/typecheck; state what wasn't run |
| No secrets | Never log, print, or commit credentials |
| Ask before destructive | `rm -rf`, force-push, drop table → confirm first |
| Update docs | Behavior change without doc update is incomplete |
| Write digest | Every meaningful session ends with a digest |
| Record assumptions | Unstated assumptions go in the digest |

## Context optimization

Retrieve only relevant memory. Do not dump the entire vault into context.
See `packages/core/standards/context-engineering.md` for retrieval hierarchy and token budgets.
