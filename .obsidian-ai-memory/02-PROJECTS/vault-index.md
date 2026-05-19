# Vault Index — CareerOS Campus AI

> Quick-lookup map of the entire `.obsidian-ai-memory/` vault.
> AI tools read this first (priority 3 in MEMORY-READ-PROTOCOL.md) to
> decide which other files to load without reading the whole vault.
> **Keep this file current.** Update it every time a session, decision, or
> error entry is added.

---

## Read protocols (read these before anything else)

| File | Purpose |
|---|---|
| `MEMORY-READ-PROTOCOL.md` | Exactly how to retrieve from this vault (modes, order, red flags) |
| `MEMORY-WRITE-PROTOCOL.md` | Exactly how to write to this vault (format, rules, commit procedure) |

---

## Project state — always load (priority 1–3)

| File | Contents | Load when |
|---|---|---|
| `02-PROJECTS/project-context.md` | Stack, architecture, constraints, next steps | Always |
| `02-PROJECTS/active-goals.md` | 5-week roadmap + current week checkboxes | Always |
| `02-PROJECTS/current-state.md` | Snapshot: exact versions, infra state, blocked | Always |

---

## Errors and anti-patterns — always load (priority 4–5)

| File | Contents | Load when |
|---|---|---|
| `03-ERRORS/error-memory.md` | Every fixed bug — symptom, root cause, fix, prevention rule | Always |
| `03-ERRORS/anti-patterns.md` | Promoted prevention rules from recurring errors | Always |

---

## Decisions — load for architecture/design tasks (priority 6)

| File | Contents |
|---|---|
| `04-DECISIONS/decisions.md` | 5 active decisions with rationale. Also see `docs/adr/` |

Current decision count: **5**
Last decision added: 2026-05-19 — "Omnix runtime stays at .omnix/"

---

## Architecture — load for system-design tasks (priority 7)

| File | Contents |
|---|---|
| `05-ARCHITECTURE/README.md` | System diagram, data flows (student + officer loops), DB schema map, key conventions |

---

## Workflows — load for procedural tasks

| File | Contents |
|---|---|
| `06-WORKFLOWS/README.md` | Step-by-step procedures: new endpoint, new table, new service, bug fix, Intel bench, session digest |

---

## Lessons — load for debugging tasks (priority: deep mode)

| File | Contents |
|---|---|
| `07-LESSONS/debugging-lessons.md` | Hard-won lessons: git mv staging trap, blanket gitignore trap |

Current lesson count: **2**

---

## Sessions — load last 3 for context continuity (priority 8)

Most recent sessions (newest first):

| Session file | Date | Tool | Type | Key outcome |
|---|---|---|---|---|
| `01-SESSIONS/2026-05-20/session-0001-claude.md` | 2026-05-20 | claude | feature-build | W1.3 migration + W1.4 role auth + W1.5 resume parser — all Week 1 tasks done |
| `01-SESSIONS/2026-05-19/session-1800-claude.md` | 2026-05-19 | claude | docs | AI agent docs personalization + strict memory protocol |
| `01-SESSIONS/2026-05-19/session-restructure.md` | 2026-05-19 | claude | architecture | Pivot + monorepo restructure + .claude scaffolding + memory populated |
| `01-SESSIONS/2026-05-18/session-2015-omnix-init.md` | 2026-05-18 | omnix | onboarding | Omnix init scan |

Session count: **4**

---

## Templates

| File | Use for |
|---|---|
| `templates/session-digest.md` | End-of-session digest (CareerOS-specific, all fields required) |
| `templates/decision-entry.md` | Appending to `04-DECISIONS/decisions.md` |
| `templates/error-entry.md` | Appending to `03-ERRORS/error-memory.md` |

---

## How to keep this file current

After every session:
1. Add the new session to the Sessions table above (newest at top)
2. If a decision was added: increment count, update "Last decision added"
3. If a lesson was added: increment count in Lessons section
4. Update the `_Updated` date below

---

_Updated: 2026-05-19 — Phase 2 + memory protocol session._
