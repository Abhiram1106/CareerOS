# Memory Read Protocol — CareerOS Campus AI

> Canonical rules for reading `.obsidian-ai-memory/` at session start.
> Every AI tool follows this before touching any code, answering any question,
> or running any command.

---

## The law: read before you do anything

No exceptions. Reading memory first prevents:
- Repeating bugs that were already diagnosed and fixed
- Re-debating decisions that were already made
- Losing the verification state from the last session
- Picking up the wrong task

---

## Retrieval order — balanced mode (~1 500 tokens)

Always read in this order. Stop when the token budget is hit.

```
ALWAYS (load every session):
  1. .obsidian-ai-memory/02-PROJECTS/project-context.md
  2. .obsidian-ai-memory/02-PROJECTS/active-goals.md
  3. .obsidian-ai-memory/02-PROJECTS/vault-index.md
  4. .obsidian-ai-memory/03-ERRORS/error-memory.md
  5. .obsidian-ai-memory/03-ERRORS/anti-patterns.md

CONDITIONALLY (load based on task type):
  6. .obsidian-ai-memory/04-DECISIONS/decisions.md
     → load for: architecture, schema, API design, scoring formula changes

  7. .obsidian-ai-memory/05-ARCHITECTURE/<relevant file>
     → load for: architecture or system-design tasks

  8. .obsidian-ai-memory/01-SESSIONS/ — last 3 session digests
     → load for: picking up mid-task work, context continuity

  9. .obsidian-ai-memory/07-LESSONS/debugging-lessons.md
     → load for: debugging, error diagnosis tasks
```

---

## How to determine "last 3 sessions"

Read `02-PROJECTS/vault-index.md` — it lists the most recent sessions.
If vault-index is stale, list `01-SESSIONS/` directories by date (newest first)
and read the most recent 3 digests found.

---

## What to extract from the session digest

When reading a previous session digest, extract:

| Extract | Why |
|---|---|
| Verification state (tsc, Python) | Tells you if the last session left things broken |
| "Next session" tasks (items 1-3) | These are your starting point unless user says otherwise |
| Open risks / blockers | May affect your approach immediately |
| Files changed | Context for what was recently touched |
| Decisions made | Don't re-debate them |

---

## Task-type aware priority (when budget is tight)

| Task type | Load first |
|---|---|
| Debugging / error | `03-ERRORS/error-memory.md` → `project-context.md` |
| Feature build | `project-context.md` → `active-goals.md` → last session |
| Architecture / schema | `04-DECISIONS/decisions.md` → `05-ARCHITECTURE/` → `project-context.md` |
| Scoring / Intel | `04-DECISIONS/decisions.md` → `project-context.md` → last session |
| Review / refactor | `03-ERRORS/anti-patterns.md` → `project-context.md` |
| Default | Order 1–5 above, then task-specific |

---

## Emit the startup block — mandatory

After reading, emit this before any other output:

```
[CareerOS Campus AI] Stack: Next.js 14 + FastAPI + Postgres/Redis | Mode: balanced
Loaded: {list files read, comma-separated} | Known errors: {N} | Last session: {date}
Week {N} goal: {one line from active-goals.md}
Routing: {workflow} | Agents: {roles}
```

If a file was unavailable (missing or empty), say so in the startup block.
Never silently skip a required file.

---

## Red flags — stop and tell the user

Stop and explicitly flag if:

- `03-ERRORS/error-memory.md` contains an error matching the current task
  → "Known error: [title]. Previous fix: [summary]. Do you want me to apply that approach?"

- The last session digest says tests were FAILING and not yet fixed
  → "Last session left tsc/Python broken. Fixing that first before proceeding."

- `active-goals.md` shows a Week N goal that conflicts with the user's request
  → "The current active goal is X. Your request is Y. Proceeding with Y — should I update active-goals.md?"

- A decision in `04-DECISIONS/decisions.md` directly contradicts the user's request
  → "We decided [X] on [date] because [reason]. Do you want to override that decision?"

---

## Deep mode (~3 000 tokens)

Use for architecture changes, Week 4+ officer surface, Intel bench design:

```
All of balanced mode, plus:
  - 04-DECISIONS/decisions.md (full)
  - 05-ARCHITECTURE/ (all files)
  - 01-SESSIONS/ last 5 digests
  - 07-LESSONS/ (all files)
```

Announce: `[CareerOS Campus AI] Mode: deep` in the startup block.

---

## Minimal mode (~400 tokens)

Use only for: one-liner answers, read-only exploration, trivial renames.

```
  - 02-PROJECTS/project-context.md (first 30 lines only)
  - 03-ERRORS/error-memory.md (titles only, skip body)
```

Announce: `[CareerOS Campus AI] Mode: minimal` in the startup block.
