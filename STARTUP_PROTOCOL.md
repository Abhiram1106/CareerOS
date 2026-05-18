# Universal AI Startup Protocol

> Every AI tool must execute this before answering or editing on every session.

## The rule

> "When this Omnix Runtime is detected, the AI must self-orchestrate. The user only describes the goal; the AI determines the workflow, agents, context, checks, and memory updates."

## Compact execution

```
Step 1 — Detect Omnix Runtime markers
  Scan for: .obsidian-ai-memory/ · AGENTS.md · AI_RULES.md · .claude/ · .cursor/ · .windsurf/ · .cline/ · .roo/
  If found → full protocol active. If not → suggest `omnix init`.

Step 2 — Identify project type
  next.config.*          → fullstack-saas
  vite.config.* only     → frontend-only
  pyproject.toml         → backend-api (python)
  pnpm-workspace.yaml    → monorepo
  k8s/ + Dockerfile      → devops-infra
  AI SDK imports         → ai-app
  playwright.config.*    → browser-scraping

Step 3 — Retrieve memory (balanced mode by default)
  Always: 02-PROJECTS/project-context.md
  Always: 02-PROJECTS/active-goals.md
  Always: 01-SESSIONS/ last 3 digests
  Always: 03-ERRORS/error-memory.md + anti-patterns.md
  On arch work: 04-DECISIONS/decisions.md + 05-ARCHITECTURE/system-overview.md
  On debug: 07-LESSONS/debugging-lessons.md

Step 4 — Auto-route workflow
  "build/add/create"          → feature-build
  "error/broken/crash/fail"   → debugging → bug-fix
  "test failing"              → bug-fix + testing
  "review/audit"              → code-review
  "refactor/clean"            → refactor
  "deploy/ship"               → deployment
  "slow/performance"          → debugging + performance agent
  "docs/readme"               → docs-update
  "security/auth/cve"         → code-review + security agent
  "schema/migration"          → feature-build + database agent
  Empty memory                → project-onboarding

Step 5 — Activate agent roles
  frontend/UI                 → frontend, product-engineer
  API change                  → api, backend, qa
  auth/payments/secrets       → backend, security
  DB schema/migration         → database, backend
  Docker/K8s/CI-CD            → devops, sre
  architecture boundaries     → architect, reviewer
  cross-cutting feature       → fullstack, architect + relevant specialists

Step 6 — Emit startup block (required, compact)
  [Omnix Runtime] Detected: <project type> · <stack>
  [Memory] Read: <N files> · last session: <date> · active goal: <one line>
  [Workflow] → <workflow>
  [Agents] → <roles>
  [Starting] <one sentence>

Step 7 — Work

Step 8 — Completion checklist (before claiming done)
  ☐ Changed files correct and intentional
  ☐ Tests/lint/typecheck run — state result or why not
  ☐ Docs updated if behavior/setup changed
  ☐ Session digest written
  ☐ Error memory updated if bug fixed
  ☐ Decision memory updated if non-trivial choice made
  ☐ Open risks listed explicitly
```

## First-run behavior (empty memory)

1. Scan project (stack, structure, entry points).
2. Generate `02-PROJECTS/project-context.md`.
3. Generate `02-PROJECTS/current-state.md`.
4. Write first session digest (role: onboarding).
5. Ask at most 2 blocking questions. Do not stall.
