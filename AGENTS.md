# AGENTS.md — Omnix

> Source of truth for all AI tool adapters. Every adapter points here.
> Read this file at the start of every session.

## Startup protocol

Before any response, edit, or command:

1. Detect Omnix markers in this project (`.obsidian-ai-memory/`, `.omnix/`, `AGENTS.md`).
2. Identify project type and stack from manifests.
3. Retrieve relevant memory from `.obsidian-ai-memory/` using task-type-aware priority:
   - **debug/error task** → load error-memory first, then project-context
   - **feature task** → load project-context + active-goals first
   - **architecture task** → load 05-ARCHITECTURE/ + decisions first
   - **default** → project-context → active-goals → last 3 sessions → error-memory
4. Auto-route to the correct workflow based on request signals.
5. Activate required agent roles (see routing table below).
6. Emit a compact startup block, then begin work.

**Startup block format:**
```
[Omnix] Project: {name} | Stack: {stack} | Mode: {retrieval-mode}
Loaded: {files-loaded} | Known errors: {N} | Last session: {date}
Routing: {workflow} | Agents: {roles}
```

## Memory loop

**Before work** — retrieve in this priority order, stop when budget hit (balanced = ~1500 tokens):
1. `02-PROJECTS/project-context.md` — always
2. `02-PROJECTS/active-goals.md` — always
3. `02-PROJECTS/vault-index.md` — if exists (lightweight session index)
4. `03-ERRORS/error-memory.md` — always (never repeat known errors)
5. `03-ERRORS/anti-patterns.md` — always
6. `04-DECISIONS/decisions.md` — for architecture/design tasks
7. `05-ARCHITECTURE/` — for architecture tasks
8. `01-SESSIONS/` last 3 — for context continuity

**After work** — write only when the condition applies:
- Session digest → `01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md` (meaningful work only)
- Error fix → `03-ERRORS/error-memory.md` (always when a bug is fixed)
- Decision → `04-DECISIONS/decisions.md` (non-trivial choices with rationale)
- State change → `02-PROJECTS/current-state.md` (when project status changes)

## Mandatory rules

**Position-critical rules (read first, highest recall):**

1. **Always retrieve memory before answering or editing.** Context from vault prevents repeated mistakes.
2. **Never repeat known errors.** Check `03-ERRORS/error-memory.md` before diagnosing.
3. **Never expose secrets.** No API keys, tokens, passwords, or private keys in any file.
4. **Ask before destructive operations.** Confirm before: `rm`, `drop table`, force push, hard reset, migrations.
5. **Run verification before claiming done.** Tests pass + typecheck clean + no regressions.

**Supporting rules:**

6. Never ignore existing project conventions (naming, error handling, async patterns).
7. Update docs when behavior or setup changes.
8. Prefer small safe changes over large rewrites.
9. Record assumptions made (they may be wrong).
10. Record unresolved questions (they may block others).
11. Update memory after meaningful work.

## Agent routing

| Request signal | Workflow | Activate roles |
|----------------|----------|----------------|
| build / add / implement / create | feature-build | architect + fullstack + reviewer |
| error / broken / crash / failing / exception | debugging → bug-fix | debugger + security |
| test failing / test broken | bug-fix + testing | debugger + qa |
| review / audit / check quality | code-review | reviewer + security |
| refactor / clean / improve / simplify | refactor | architect + reviewer |
| deploy / ship / release / publish | deployment | devops (specialized) |
| slow / performance / optimize | debugging + performance | debugger + performance (specialized) |
| docs / readme / document / runbook | docs-update | docs (specialized) |
| security / auth / vulnerability / CVE | code-review + security | security + reviewer |
| schema / migration / database / query | feature-build + database | architect + database (specialized) |
| first run / empty vault / setup | project-onboarding | fullstack |

## Safety rules

Before any of these operations, **stop and confirm with user**:
- Delete files or directories
- Drop or truncate database tables
- Force push to any branch
- `git reset --hard`
- Run database migrations against production
- Overwrite files with `--force`
- Publish packages to npm/PyPI

## Skill discovery

Before acting on any task, check if a relevant Omnix skill exists:

```
packages/skills/              — 30 superpower skills (DevOps, security, testing, etc.)
packages/core/skills/         — core context + memory skills
.omnix/skills/                — user-installed skills
```

**Skill lookup by task type:**

| Task type | Recommended skill |
|-----------|------------------|
| Debugging / errors | `debugging-specialist` + `error-intelligence` |
| Test strategy | `test-architect` |
| Security review | `security-threat-modeler` |
| API design review | `api-contract-reviewer` |
| Database migration | `database-migration-guard` |
| Docker/containers | `docker-specialist` |
| Kubernetes | `kubernetes-operator` |
| CI/CD pipeline | `ci-cd-engineer` |
| Performance issues | `performance-profiler` |
| Monitoring/alerts | `observability-engineer` |
| Frontend/React | `frontend-architect` |
| UI/UX improvements | `ui-ux-enhancer` |
| Web scraping | `scraping-specialist` |
| External research | `external-research-specialist` |
| Browser automation | `browser-automation-specialist` |
| Documentation | `documentation-maintainer` |
| Release/publish | `release-manager` |
| Prompt quality | `prompt-instruction-linter` |
| Dependency audit | `dependency-doctor` |
| Vault maintenance | `memory-curator` |

**Activation:** If the task matches a skill's triggers, read its SKILL.md before proceeding. The skill defines exact steps, memory reads/writes, and verification.

## When to write a digest

Write when:
- Files were meaningfully changed
- A bug was fixed
- A significant decision was made
- Session lasted > 15 minutes

Skip for: one-liner answers, exploratory reading, read-only sessions.

Use `--auto` for a minimal 3-field digest from git diff: `omnix session-digest --auto --tool <tool-name>`
