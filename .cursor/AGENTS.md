# .cursor/AGENTS.md — CareerOS Campus AI

> Cursor-specific agent configuration.
> Project-shared and committed. Personal overrides in `.cursor/AGENTS.local.md` (gitignored).
> For the universal startup protocol and routing table, see root `AGENTS.md`.

## Cursor startup behaviour

On every new session Cursor should:

1. Load `.cursorrules` (auto-loaded from repo root).
2. Load applicable rules from `.cursor/rules/` based on active file type.
3. Read memory from `.obsidian-ai-memory/` in the order defined in `STARTUP_PROTOCOL.md`.
4. Reference the context files in `.cursor/context/` when working in specific areas.
5. Emit the startup block, then begin work.

## Always-include context files

Use `@file` or add to Cursor's "always include" for these files when working in the
area they describe:

| Working in | Context file to include |
|---|---|
| Any backend service | `.cursor/context/backend-context.md` |
| `apps/web/` frontend | `.cursor/context/frontend-context.md` |
| Database / Alembic | `.cursor/context/database-context.md` |
| Scoring / Intel | `.cursor/context/scoring-intel-context.md` |
| AI rewriter / guardrails | `.cursor/context/rewriter-context.md` |

## Agent modes

### Feature-build mode
Triggered by: build / add / implement / create

Steps:
1. Read `active-goals.md` — confirm task matches current week
2. Read relevant context file from `.cursor/context/`
3. Check `error-memory.md` for known bugs in the area
4. Implement → verify (tsc / Python AST) → write session digest

### Debug mode
Triggered by: error / broken / crash / exception / failing

Steps:
1. Read `error-memory.md` FIRST — check if this exact bug was seen before
2. Read `anti-patterns.md` — apply prevention rules
3. Read `07-LESSONS/debugging-lessons.md` (deep mode)
4. Reproduce → fix → add regression test → append to `error-memory.md`

### Architecture mode
Triggered by: schema / migration / database / new service / redesign

Steps:
1. Read `04-DECISIONS/decisions.md`
2. Read `05-ARCHITECTURE/README.md`
3. Check relevant ADR in `docs/adr/`
4. Design → write ADR if non-trivial → implement

### Review mode
Triggered by: review / audit / quality

Steps:
1. Read `03-ERRORS/anti-patterns.md`
2. Check against `.cursor/rules/` for the relevant file type
3. Report violations with file + line; do not auto-fix unless asked

## Cursor-specific capabilities to use

- **`@codebase`** for broad context when implementing cross-cutting features
- **`@file`** to pin specific context files (use the `.cursor/context/` files)
- **Composer** for multi-file changes (prefer over chat for implementation tasks)
- **Agent mode** for autonomous multi-step tasks (debug + fix + test cycles)
- **Inline edit** for single-function changes

## Memory write after every session

Cursor must write a session digest to:
`.obsidian-ai-memory/01-SESSIONS/YYYY-MM-DD/session-HHMM-cursor.md`

Then commit:
```bash
git add .obsidian-ai-memory/
git commit -m "memory: YYYY-MM-DD session digest (cursor)"
```

See `MEMORY-WRITE-PROTOCOL.md` for the full format.
