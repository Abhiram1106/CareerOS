# Startup Protocol — CareerOS Campus AI

> Every AI tool (Claude Code, Cursor, Copilot, Omnix) executes this protocol
> before answering or editing — every session, no exceptions.
> Full read rules: `.obsidian-ai-memory/MEMORY-READ-PROTOCOL.md`
> Full write rules: `.obsidian-ai-memory/MEMORY-WRITE-PROTOCOL.md`

---

## Step 1 — Detect project

Confirm markers: `AGENTS.md` + `.obsidian-ai-memory/` + `pnpm-workspace.yaml` + `services/core-api/`

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

## Step 3 — Retrieve memory (READ FIRST, always)

Read in this order. Stop at ~1 500-token budget (balanced mode).
See `MEMORY-READ-PROTOCOL.md` for the full retrieval rules, modes, and red flags.

**Always load (every session):**

```text
1. .obsidian-ai-memory/02-PROJECTS/project-context.md
2. .obsidian-ai-memory/02-PROJECTS/active-goals.md
3. .obsidian-ai-memory/02-PROJECTS/vault-index.md
4. .obsidian-ai-memory/03-ERRORS/error-memory.md
5. .obsidian-ai-memory/03-ERRORS/anti-patterns.md
```

**Load for architecture / design / schema tasks:**

```text
6. .obsidian-ai-memory/04-DECISIONS/decisions.md
7. .obsidian-ai-memory/05-ARCHITECTURE/README.md
```

**Load for context continuity (picking up mid-task work):**

```text
8. .obsidian-ai-memory/01-SESSIONS/ — last 3 session digests
   (use vault-index.md to find the most recent ones)
```

**Load for debugging tasks:**

```text
9. .obsidian-ai-memory/07-LESSONS/debugging-lessons.md
```

**Red flags — stop and surface these to the user before proceeding:**
- A known error in `error-memory.md` matches the current task
- The last session digest says tests were FAILING and not yet fixed
- A decision in `decisions.md` directly contradicts the user's request

---

## Step 4 — Emit startup block (required, every session)

```text
[CareerOS Campus AI] Stack: Next.js 14 + FastAPI + Postgres/Redis | Mode: {balanced|deep|minimal}
Loaded: {comma-separated list of files actually read} | Known errors: {N} | Last session: {date}
Week {N} goal: {one-line from active-goals.md}
Routing: {workflow} | Agents: {roles}
```

State explicitly if a required file was missing or empty.

---

## Step 5 — Work

Follow `AI_RULES.md` and the scoped rules in `.claude/rules/` or `.cursor/rules/`.

**Apply these conventions automatically — without being asked:**

- FastAPI route handlers stay slim — logic in `services/<svc>/app/services/`
- All cross-service HTTP via `services/core-api/app/services/clients.py` (httpx)
- All web HTTP via `apps/web/lib/api.ts` — never `fetch()` inline
- SQLAlchemy 2.0: `Mapped[T]` / `mapped_column(...)` — no legacy `Column()`
- Pydantic v2: `model_dump()` not `.dict()`
- React: `"use client"` only when strictly necessary (hooks / browser APIs)
- No Tailwind, no shadcn — custom CSS variables in `apps/web/app/globals.css`
- UI primitives: `CardSection`, `FormField`, `MetricTile` from `apps/web/components/ui/primitives.tsx`
- Score formula imported from `packages/scoring/` — never inlined or duplicated
- Schema change → write Alembic migration — never `entities.py` alone

---

## Step 6 — Completion checklist

Before saying "done" — check every item and state the result:

- [ ] Changed files are correct and match intent
- [ ] `tsc --noEmit` on `apps/web` — state: passed / failed / skipped (reason)
- [ ] Python AST-parse on all touched `services/*.py` — state: passed / failed / skipped
- [ ] Alembic migration written if schema changed (not just `entities.py`)
- [ ] Docs updated if behaviour or API changed
- [ ] No secrets in any written file
- [ ] Open risks explicitly listed
- [ ] Session digest written (Step 7 below)
- [ ] Error memory appended if bug was fixed
- [ ] Decision log appended if non-trivial choice was made
- [ ] Vault-index updated if session/error/decision was added

---

## Step 7 — Write session digest (MANDATORY for meaningful sessions)

**A session is meaningful if:** files changed, bug fixed, decision made, or session > 15 min.
**Skip only for:** one-liner answers, read-only exploration, trivial formatting fixes.

**File path:** `.obsidian-ai-memory/01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md`

Where `<tool>` = `claude` | `cursor` | `copilot` | `omnix`

**Use `templates/session-digest.md`.** All fields required. Write "none" or "N/A" explicitly.

**Minimum viable digest:**

```markdown
# Session — {one-line title}

Date: YYYY-MM-DD HH:MM IST | Tool: claude | Type: {feature-build|bug-fix|...}
Week goal: {from active-goals.md}

## What landed
- {one bullet per meaningful file change}

## Verification
- tsc --noEmit: passed | failed | skipped (reason)
- Python AST: passed | failed | skipped (reason)

## Decisions made
- {any non-trivial choices — also append to 04-DECISIONS/decisions.md}

## Errors fixed
- {any bugs — also append to 03-ERRORS/error-memory.md}

## Open risks
- {anything that may block next session}

## Next session — top 3 tasks
1. {concrete task}
2. {concrete task}
3. {concrete task}
```

---

## Step 8 — Commit the vault (MANDATORY after every digest)

After writing the digest and any error/decision updates:

```bash
git add .obsidian-ai-memory/
git commit -m "memory: YYYY-MM-DD {brief description of session}"
```

Rules:
- Use prefix `memory:` — keeps vault commits filterable from code commits
- This is a **separate commit** from the code commit
- Commit even if only the session digest was written — the next tool needs it
- Push to origin so every AI tool on every platform gets the update

**The vault commit is what makes cross-platform development work.**
Claude Code ends a session → commits vault → Cursor starts a session →
reads vault → picks up exactly where Claude left off.
