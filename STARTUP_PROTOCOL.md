# Startup Protocol — CareerOS Campus AI

> Every AI tool executes this protocol before answering or editing on every session.
> Adapters: Claude Code · Cursor · Copilot · Omnix

---

## Step 1 — Detect project

Look for: `AGENTS.md` + `.obsidian-ai-memory/` + `pnpm-workspace.yaml` + `services/core-api/`

If found → full protocol active.
If not → wrong directory; stop and tell the user.

---

## Step 2 — Identify task type

| Signal in the user's message | Task type |
|---|---|
| resume / parse / pdfplumber / docx / section | feature-build (parser) |
| match / TF-IDF / embedding / cosine / sklearnex | feature-build (match-engine) |
| score / readiness / formula / ATS / penalty | feature-build (scoring) |
| rewrite / proof-linked / fabrication / guardrail | feature-build (rewriter) |
| officer / dashboard / batch / heatmap / cohort | feature-build (officer surface) |
| OpenVINO / benchmark / latency / throughput | perf + intel |
| alembic / migration / schema / new table | feature-build + database |
| auth / JWT / role / RBAC / DPDP | security + feature-build |
| error / broken / crash / exception / failing | debug → bug-fix |
| tsc / type error / TypeScript | bug-fix (frontend) |
| review / audit / quality | code-review |
| refactor / clean / simplify | refactor |
| deploy / docker / compose | deployment |
| docs / ADR / README | docs-update |

---

## Step 3 — Retrieve memory

Always retrieve (stop at ~1 500 tokens):

```
1. .obsidian-ai-memory/02-PROJECTS/project-context.md
2. .obsidian-ai-memory/02-PROJECTS/active-goals.md
3. .obsidian-ai-memory/02-PROJECTS/vault-index.md
4. .obsidian-ai-memory/03-ERRORS/error-memory.md
5. .obsidian-ai-memory/03-ERRORS/anti-patterns.md
```

Additionally for architecture/design tasks:
```
6. .obsidian-ai-memory/04-DECISIONS/decisions.md
7. .obsidian-ai-memory/05-ARCHITECTURE/ (if populated)
```

Additionally for context continuity:
```
8. .obsidian-ai-memory/01-SESSIONS/ — last 3 session digests
```

---

## Step 4 — Emit startup block

```
[CareerOS Campus AI] Stack: Next.js 14 + FastAPI + Postgres/Redis | Mode: balanced
Loaded: {N files} | Known errors: {N} | Last session: {date}
Week {N} goal: {one-line from active-goals.md}
Routing: {workflow} | Agents: {roles}
```

---

## Step 5 — Work

Follow rules in `AI_RULES.md` and `.claude/rules/` (or `.cursor/rules/`) for the
file type being edited.

**Key project conventions to apply without being asked:**

- FastAPI route handlers stay slim — logic in `services/<svc>/app/services/`
- All cross-service HTTP calls via `services/core-api/app/services/clients.py`
- All web HTTP calls via `apps/web/lib/api.ts`
- SQLAlchemy 2.0 mapped-column style (`Mapped[T]` / `mapped_column(...)`)
- Pydantic v2 (`model_dump()` not `.dict()`)
- React: `"use client"` only when strictly necessary
- No Tailwind, no shadcn, no styled-components — custom CSS in `globals.css`
- UI primitives: `CardSection`, `FormField`, `MetricTile` in `apps/web/components/ui/primitives.tsx`
- Score formula imported from `packages/scoring/` — never duplicated

---

## Step 6 — Completion checklist

Before saying "done":

- [ ] Changed files are correct and match intent
- [ ] `tsc --noEmit` clean on `apps/web` (state result or explain why skipped)
- [ ] Python files AST-parse / import clean on `services/*` (state result)
- [ ] Alembic migration written if schema changed (not just entities.py)
- [ ] Docs updated if behaviour or setup changed
- [ ] No secrets in any written file
- [ ] Open risks listed if any remain
- [ ] Session digest written (skip only for read-only sessions)
- [ ] Error memory updated if a bug was fixed
- [ ] Decision memory updated if a non-trivial choice was made

---

## Step 7 — Write session digest

File: `.obsidian-ai-memory/01-SESSIONS/YYYY-MM-DD/session-HHMM-claude.md`

Minimum fields:

```markdown
# Session — {one-line title}

**Date**: YYYY-MM-DD
**Tool**: Claude Code
**Week goal**: {from active-goals.md}

## What landed
- {bullet per meaningful change}

## Decisions made
- {any non-trivial choices}

## Errors fixed
- {any bugs; also update error-memory.md}

## Open risks
- {anything that may block next session}

## Next session
- {top 3 concrete next steps}
```

Skip the digest only for: one-liner answers, read-only exploration, trivial
formatting fixes.
