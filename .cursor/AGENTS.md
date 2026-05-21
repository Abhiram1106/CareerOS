# .cursor/AGENTS.md — CareerOS Campus AI

> Cursor-specific agent configuration.
> Project-shared and committed. Personal overrides in `.cursor/AGENTS.local.md` (gitignored).
> For the universal startup protocol and routing table, see root `AGENTS.md`.

## Cursor startup behaviour

On every new **chat** (conversation), before the first substantive reply:

1. Load `.cursorrules` (auto-loaded from repo root).
2. Load applicable rules from `.cursor/rules/` (`project-rules.mdc`, `memory-session.mdc`, area rules).
3. Read **`.obsidian-ai-memory/02-PROJECTS/session-continuity.md`** — rolling handoff from the previous chat.
4. Read memory from `.obsidian-ai-memory/` in the order defined in root `AGENTS.md` (Memory loop).
5. Read the **latest** `01-SESSIONS/.../session-*-cursor.md` file(s) referenced in continuity.
6. Reference `.cursor/context/` when working in specific areas.
7. Emit the startup block, then begin work.

## Cursor shutdown behaviour (end of every chat)

**Mandatory** unless read-only Q&A with no handoff. Full steps: **`.cursor/MEMORY-WORKFLOW.md`**.

Summary:

1. Write or append session digest → `01-SESSIONS/YYYY-MM-DD/session-HHMM-cursor.md`
2. Overwrite rolling handoff → `02-PROJECTS/session-continuity.md`
3. Update `vault-index.md`, `current-state.md`, architecture/errors as needed
4. `git commit` vault only: `memory: YYYY-MM-DD cursor — <summary>`
5. End user message with a **Memory** section (paths + commit hash)

This enables **chat-to-chat traceability** without relying on Cursor’s built-in transcript alone.

## Always-include context files

Use `@file` or add to Cursor's "always include" (`cursor-settings.json`):

| Working in | Context file to include |
|---|---|
| Any session start | `.obsidian-ai-memory/02-PROJECTS/session-continuity.md` |
| Any backend service | `.cursor/context/backend-context.md` |
| `apps/web/` frontend | `.cursor/context/frontend-context.md` |
| Database / Alembic | `.cursor/context/database-context.md` |
| Scoring / Intel | `.cursor/context/scoring-intel-context.md` |
| AI rewriter / guardrails | `.cursor/context/rewriter-context.md` |

## Agent modes

### Feature-build mode
Triggered by: build / add / implement / create

Steps:
1. Read `session-continuity.md` + `active-goals.md` — confirm task matches current week
2. Read relevant context file from `.cursor/context/`
3. Check `error-memory.md` for known bugs in the area
4. Implement → verify (tsc / Python AST) → **shutdown protocol** (digest + continuity + commit)

### Debug mode
Triggered by: error / broken / crash / exception / failing

Steps:
1. Read `error-memory.md` FIRST — check if this exact bug was seen before
2. Read `anti-patterns.md` — apply prevention rules
3. Reproduce → fix → append `error-memory.md` → **shutdown protocol**

### Architecture mode
Triggered by: schema / migration / database / new service / redesign

Steps:
1. Read `04-DECISIONS/decisions.md`
2. Read `05-ARCHITECTURE/README.md` + `layered-modules.md`
3. Check relevant ADR in `docs/adr/`
4. Design → write ADR if non-trivial → implement → **shutdown protocol**

### Review mode
Triggered by: review / audit / quality

Steps:
1. Read `03-ERRORS/anti-patterns.md`
2. Check against `.cursor/rules/` for the relevant file type
3. Report violations with file + line; **shutdown protocol** if vault/docs updated

## Cursor-specific capabilities to use

- **`@codebase`** for broad context when implementing cross-cutting features
- **`@file`** to pin `session-continuity.md` and `.cursor/context/` files
- **Composer** for multi-file changes (prefer over chat for implementation tasks)
- **Agent mode** for autonomous multi-step tasks (debug + fix + test cycles)

## Memory files (quick reference)

| File | Purpose |
|------|---------|
| `02-PROJECTS/session-continuity.md` | Rolling snapshot — **read first** each chat |
| `01-SESSIONS/.../session-HHMM-cursor.md` | Per-chat audit trail |
| `MEMORY-WRITE-PROTOCOL.md` | Cross-tool write rules |
| `.cursor/MEMORY-WORKFLOW.md` | Cursor-specific startup/shutdown |
