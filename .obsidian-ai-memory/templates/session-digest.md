# Session Digest — CareerOS Campus AI

<!-- Copy this file to 01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md -->
<!-- Fill every field. Empty fields are not allowed. Use "none" or "N/A" explicitly. -->

---

## Header

| Field | Value |
|---|---|
| Date | YYYY-MM-DD |
| Time | HH:MM IST |
| Tool | claude-code \| cursor \| copilot \| omnix |
| Session type | feature-build \| bug-fix \| refactor \| docs \| architecture \| review \| perf \| infra |
| Week goal | (one line from active-goals.md) |
| User request | (verbatim or close paraphrase of what was asked) |

---

## Memory retrieved at session start

List every vault file actually read. Do NOT list files you intended to read but skipped.

- [ ] `02-PROJECTS/project-context.md`
- [ ] `02-PROJECTS/active-goals.md`
- [ ] `02-PROJECTS/vault-index.md`
- [ ] `03-ERRORS/error-memory.md`
- [ ] `03-ERRORS/anti-patterns.md`
- [ ] `04-DECISIONS/decisions.md` (if arch task)
- [ ] `01-SESSIONS/` last 3 (if continuity needed)
- Other: ___

Known errors at session start: (N or list)

---

## Work done

### Files changed

| File | Change type | Summary |
|---|---|---|
| `path/to/file` | created \| modified \| deleted | one-line description |

### Commands run

```
# list significant shell/CLI commands
```

### Verification

- TypeScript (`tsc --noEmit`): passed \| failed \| skipped (reason)
- Python AST parse (`services/*`): passed \| failed \| skipped (reason)
- Alembic (`upgrade head` on clean DB): passed \| skipped \| N/A
- Other tests: ___

---

## Decisions made

List any non-trivial choice made during the session. Also append to `04-DECISIONS/decisions.md`.

- **Decision**: ___
  **Rationale**: ___
  **Alternatives rejected**: ___

---

## Errors encountered and fixed

For each error also append to `03-ERRORS/error-memory.md`.

- **Error**: ___
  **Root cause**: ___
  **Fix**: ___
  **Prevention rule**: ___
  **Regression test added**: yes \| no \| N/A

---

## Memory written after session

Check every item that was actually written (not just planned).

- [ ] This session digest committed to `01-SESSIONS/YYYY-MM-DD/`
- [ ] `03-ERRORS/error-memory.md` updated (if bug fixed)
- [ ] `04-DECISIONS/decisions.md` updated (if decision made)
- [ ] `02-PROJECTS/current-state.md` updated (if state changed)
- [ ] `02-PROJECTS/active-goals.md` checkbox updated
- [ ] `02-PROJECTS/vault-index.md` updated (if new session/decision/error added)

---

## Open risks / blockers

Things that may block the next session. Be specific.

- ___

---

## Next session — top 3 concrete tasks

1. ___
2. ___
3. ___

---

## Cross-platform handoff note

> This digest is the single source of truth for any AI tool picking up this work.
> The next session MUST read this file (via `01-SESSIONS/` last-3 retrieval) before touching any code.
> Active week goal, verification state, and open risks above are the minimum context required.
