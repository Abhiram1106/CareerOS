# Memory Write Protocol — CareerOS Campus AI

> Canonical rules for writing to `.obsidian-ai-memory/`.
> Every AI tool (Claude Code, Cursor, Copilot, Omnix) follows this exactly.
> Cross-platform consistency depends on every tool writing identical structure.

---

## The law: write after EVERY meaningful session

A session is "meaningful" if any of these are true:
- One or more files were created or modified
- A bug was found and fixed
- A non-trivial architectural or implementation decision was made
- The session lasted more than 15 minutes

If none of the above — skip the digest. Do not write empty or trivial entries.

---

## What to write and when

| Trigger | File to update | Action |
|---|---|---|
| End of any meaningful session | `01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md` | Create from template |
| Bug fixed | `03-ERRORS/error-memory.md` | **Append** one entry (never overwrite) |
| Non-trivial decision made | `04-DECISIONS/decisions.md` | **Append** one entry |
| Project phase or state changes | `02-PROJECTS/current-state.md` | Overwrite (it's a snapshot) |
| Week goal checkbox completed | `02-PROJECTS/active-goals.md` | Check the `[ ]` → `[x]` |
| New session/error/decision added | `02-PROJECTS/vault-index.md` | Update the "Most recent" line |

---

## Session digest — strict format

**File path**: `.obsidian-ai-memory/01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md`

Where:
- `YYYY-MM-DD` = date in IST
- `HHMM` = 24h time the session ended (approximate)
- `<tool>` = `claude` | `cursor` | `copilot` | `omnix`

**Example**: `01-SESSIONS/2026-05-20/session-1430-claude.md`

**Content**: use `templates/session-digest.md`. All fields are required.
Explicitly write "none" or "N/A" — never leave a field blank.

**Minimum viable digest** (when time is short):
```markdown
# Session — {one-line title}
Date: YYYY-MM-DD HH:MM | Tool: claude | Type: {type}
Week goal: {from active-goals.md}

## What landed
- {bullet per meaningful file change}

## Verification
- tsc: passed | failed | skipped
- Python AST: passed | failed | skipped

## Next session
1. {task 1}
2. {task 2}
3. {task 3}
```

Even the minimum digest MUST include: date, tool, what landed, verification state, and next 3 tasks.

---

## Error memory — strict format

**File**: `03-ERRORS/error-memory.md`
**Rule**: APPEND ONLY. Never delete or overwrite existing entries.

Each entry uses the structure in `templates/error-entry.md`:
- Symptom (exact error message if possible)
- Root cause (precise enough for future pattern-matching)
- Fix (file paths + what changed)
- Prevention rule (one imperative sentence)
- Do not repeat (the single most important thing to remember)

---

## Decision log — strict format

**File**: `04-DECISIONS/decisions.md`
**Rule**: APPEND ONLY.

Each entry uses `templates/decision-entry.md`.
For architectural decisions, also create `docs/adr/NNNN-title.md`.
Reference the ADR from the decision entry.

---

## What NEVER goes in memory

| Do NOT write | Why |
|---|---|
| Raw code snippets | Code lives in the repo — memory stores context, not implementation |
| JWT secrets, DB passwords, API keys | Obvious |
| Duplicate entries for the same bug/decision | Vault becomes noise |
| Speculative "might happen" entries | Only write what actually happened |
| Trivial sessions (< 15 min, read-only) | Adds noise, dilutes retrieval signal |
| Full stack traces | Summarise: symptom + cause + fix |
| Absolute Windows paths to user home | Use relative vault paths |

---

## After writing — always do this

1. Update `02-PROJECTS/vault-index.md` "Most recent session" and counts.
2. Check the active goal checkbox in `02-PROJECTS/active-goals.md` if a goal completed.
3. Run `git add .obsidian-ai-memory/ && git commit -m "memory: {date} session digest + updates"`.

**The memory commit is a separate commit from the code commit.**
Use prefix `memory:` so it is easy to filter from code history.

---

## Cross-platform handoff guarantee

When this protocol is followed correctly, any AI tool that reads the vault
at the start of the next session will have:

- The exact verification state (did tests pass?)
- The exact next 3 tasks to pick up
- Any bugs found (so they are not rediscovered)
- Any decisions made (so they are not re-debated)
- The current week goal and checkbox state

This is the contract that makes cross-platform development coherent.
