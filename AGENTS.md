# AGENTS.md — CareerOS Campus AI

> Source of truth for all AI tool adapters (Claude Code, Cursor, Copilot, Omnix).
> Every adapter reads this file at session start before doing anything else.

## Startup protocol

1. Confirm repo markers: `AGENTS.md` + `.obsidian-ai-memory/` + `pnpm-workspace.yaml` + `services/core-api/`
2. Read memory in priority order (see Memory loop).
3. Route to the correct workflow.
4. Activate agent roles.
5. Emit the startup block, then begin work.

**Startup block (emit every session):**
```
[CareerOS Campus AI] Stack: Next.js 14 + FastAPI + Postgres/Redis | Mode: {mode}
Loaded: {files} | Known errors: {N} | Last session: {date}
Week {N} goal: {one-line from active-goals.md}
Routing: {workflow} | Agents: {roles}
```

---

## Memory loop

**Before work** — retrieve in order, stop at ~1 500-token budget:

| # | File | Load when |
|---|---|---|
| 1 | `.obsidian-ai-memory/02-PROJECTS/project-context.md` | always |
| 2 | `.obsidian-ai-memory/02-PROJECTS/active-goals.md` | always |
| 3 | `.obsidian-ai-memory/02-PROJECTS/vault-index.md` | always |
| 4 | `.obsidian-ai-memory/03-ERRORS/error-memory.md` | always |
| 5 | `.obsidian-ai-memory/03-ERRORS/anti-patterns.md` | always |
| 6 | `.obsidian-ai-memory/04-DECISIONS/decisions.md` | architecture / design tasks |
| 7 | `.obsidian-ai-memory/05-ARCHITECTURE/` | architecture tasks |
| 8 | `.obsidian-ai-memory/01-SESSIONS/` last 3 | context continuity |

**After work — STRICT write enforcement:**

The memory write is **not optional**. Every meaningful session ends with
a committed vault update. See `MEMORY-WRITE-PROTOCOL.md` for the full
format. The short rules:

| Condition | Write to | How |
|---|---|---|
| Meaningful files changed | `01-SESSIONS/YYYY-MM-DD/session-HHMM-<tool>.md` | Create from template |
| Bug fixed | `03-ERRORS/error-memory.md` | Append — never overwrite |
| Non-trivial decision | `04-DECISIONS/decisions.md` | Append — never overwrite |
| Project state changed | `02-PROJECTS/current-state.md` | Overwrite (it's a snapshot) |
| Goal completed | `02-PROJECTS/active-goals.md` | Mark `[ ]` → `[x]` |
| Any of the above | `02-PROJECTS/vault-index.md` | Update session table + counts |

**After writing — always commit the vault:**
```
git add .obsidian-ai-memory/
git commit -m "memory: YYYY-MM-DD session digest [+ error/decision if applicable]"
```
Use prefix `memory:` so vault commits are easy to filter from code commits.

**Cross-platform guarantee**: when this protocol is followed, any AI tool
(Claude Code, Cursor, Copilot) picking up the next session will have exact
verification state, next 3 tasks, any new bugs, and any new decisions —
without the user needing to re-explain anything.

---

## Mandatory rules

1. **Memory first.** Read vault before any response or edit. Prevents repeated mistakes.
2. **No repeated errors.** Check `03-ERRORS/error-memory.md` before diagnosing anything.
3. **No secrets.** No JWT secrets, DB passwords, API keys, or private keys in any file — not even in comments.
4. **Confirm before destructive ops.** Stop and ask before: `rm`, `DROP TABLE`, force push, `git reset --hard`, Alembic on non-empty DB.
5. **Verify before "done".** `tsc --noEmit` clean on `apps/web`. All `services/*.py` AST-parse (or import) clean. State result explicitly.
6. **No fabrication in rewriter.** `services/ai-rewriter` must never invent metrics, tools, certifications, internships, or team size. Flag them in `unsupported_claims[]`.
7. **Score formula in `packages/scoring/` only.** Never duplicate PlacementReadinessScore in service code — import the shared package.
8. **One concern per commit.** No WIP or "broken" commits on `main`.
9. **Update docs with behaviour changes.** Changed endpoint without updated README or ADR is incomplete.
10. **Write a session digest** after sessions > 15 min or with meaningful changes.

---

## Routing table — CareerOS-specific signals

| Signal | Workflow | Roles |
|---|---|---|
| resume-parser / pdfplumber / section extractor | feature-build + database | backend + architect + reviewer |
| match-engine / TF-IDF / embeddings / sklearnex | feature-build + intel | backend + data-science + reviewer |
| officer dashboard / batch / readiness heatmap | feature-build + frontend | frontend + backend + reviewer |
| intel-bench / OpenVINO / benchmark / latency | perf + intel | data-science + devops + reviewer |
| placement readiness score / scoring formula | feature-build | backend + data-science |
| proof-linked rewrite / AI rewriter / guardrails | feature-build | backend + security + reviewer |
| alembic / migration / schema / new table | feature-build + database | database + backend |
| JWT / role / RBAC / auth gate | feature-build + security | security + backend |
| DPDP / audit log / consent / retention | code-review + security | security + reviewer |
| ATS parse safety / heuristics / penalty | feature-build | backend + reviewer |
| pane / component / UI / officer surface | feature-build + frontend | frontend + reviewer |
| tsc error / type error / TypeScript | bug-fix | frontend + reviewer |
| error / broken / crash / exception | debug → bug-fix | debugger + security |
| slow / performance / optimize | debug + perf | data-science + devops |
| review / audit / quality | code-review | reviewer + security |
| refactor / clean / simplify | refactor | architect + reviewer |
| docker / compose / deploy | deployment | devops |
| docs / ADR / README / runbook | docs-update | docs |

---

## Stack map (use for glob/routing accuracy)

| Layer | Tech | Canonical path |
|---|---|---|
| Web app | Next.js 14 app router, TypeScript strict, no Tailwind | `apps/web/` |
| Web panes | React client components, `useCareerOSWorkspace` hook | `apps/web/components/panes/` |
| UI primitives | `CardSection`, `FormField`, `MetricTile` | `apps/web/components/ui/primitives.tsx` |
| API client | Typed `lib/api.ts` — never `fetch()` inline in components | `apps/web/lib/api.ts` |
| Types | `ActivePane`, `Scan`, `Dashboard`, `History`, `ResumeItem` | `apps/web/components/panes/types.ts` |
| Core API | FastAPI 0.115, SQLAlchemy 2.0 mapped-column, Pydantic v2 | `services/core-api/app/main.py` |
| Auth | JWT (python-jose), Bearer, SessionTokens table | `services/core-api/app/services/auth.py` |
| DB models | SQLAlchemy mapped-column style | `services/core-api/app/models/entities.py` |
| Pydantic schemas | Pydantic v2 BaseModel + EmailStr | `services/core-api/app/schemas/contracts.py` |
| Service clients | httpx async calls to downstream services | `services/core-api/app/services/clients.py` |
| Config | `os.getenv()` + fallbacks, validated at startup | `services/core-api/app/config.py` |
| Celery tasks | PDF export task; Redis broker | `services/core-api/app/workers/tasks.py` |
| PDF export | WeasyPrint (disabled on Windows; use Docker) | `services/core-api/app/services/pdf_export.py` |
| Migrations | Alembic — real migration files, not `AUTO_CREATE_TABLES` | `services/core-api/migrations/versions/` |
| ATS engine | Rule-based parse-safety scorer (becomes ATS_Parse_Safety sub-score) | `services/ats-engine/app/main.py` |
| AI rewriter | Proof-linked rewriter, JSON schema output (Week 3 retarget) | `services/ai-rewriter/app/main.py` |
| Resume parser | pdfplumber + python-docx + spaCy (Week 1 build) | `services/resume-parser/` (pending) |
| Match engine | TF-IDF + sentence-transformers + sklearnex (Week 2 build) | `services/match-engine/` (pending) |
| Intel bench | OpenVINO + sklearnex harness (Week 5 build) | `services/intel-bench/` (pending) |
| Scoring pkg | PlacementReadinessScore formula — shared lib | `packages/scoring/` (pending) |
| Contracts | JSON Schema (Resume, JD, Scorecard, Rewrite) + OpenAPI | `packages/contracts/` |

---

## Safety gates

Stop and confirm before any of:
- Deleting files or directories
- Dropping or truncating database tables
- Running Alembic on a non-empty database
- Force-pushing any branch
- `git reset --hard`
- Writing real values to `.env` or `.env.example`
- Publishing to PyPI or npm
