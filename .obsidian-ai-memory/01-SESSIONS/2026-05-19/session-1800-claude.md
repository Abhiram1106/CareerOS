# Session — AI agent docs personalization + strict memory protocol

Date: 2026-05-19 ~18:00 IST | Tool: claude | Type: docs + architecture
Week goal: Phase 2 complete — monorepo scaffold, .claude, Omnix memory populated

---

## Memory retrieved at session start

- [x] `02-PROJECTS/project-context.md`
- [x] `02-PROJECTS/active-goals.md`
- [x] `02-PROJECTS/vault-index.md`
- [x] `03-ERRORS/error-memory.md`
- [x] `03-ERRORS/anti-patterns.md`
- [ ] `04-DECISIONS/decisions.md` — not loaded (docs session)
- [ ] `01-SESSIONS/` last 3 — continuity loaded from prior session in same day

Known errors at session start: 4 (git mv staging, blanket gitignore, parallel rewrite, tsbuildinfo)

---

## Work done

### Files changed

| File | Change type | Summary |
|---|---|---|
| `AGENTS.md` | modified | Full rewrite: CareerOS-specific routing table, stack map, skill lookup, strict write enforcement in memory loop |
| `AI_RULES.md` | modified | Three concrete rule sections (Python/TS/Intel), all referencing actual file paths |
| `PROJECT_CONTEXT.md` | modified | Filled all (fill in) stubs: stack, phase, plan, ADRs, "what this is NOT", 7-step demo workflow |
| `STARTUP_PROTOCOL.md` | modified | Step 2 signal table, Step 3 4-group retrieval + red flags, Step 7 mandatory digest, Step 8 vault commit |
| `.claude/CLAUDE.md` | modified | 18-entry key-project-paths quick-nav table |
| `.claude/rules/code-style.md` | modified | Python + TypeScript merged, all conventions with exact file paths |
| `.claude/rules/frontend/react.md` | modified | Route group plan, Week 4 hook split, no-Tailwind constraint with ADR gate |
| `.claude/settings.json` | modified | Stop hook (memory write reminder) + PreToolUse/Bash hook |
| `.cursor/rules/*.mdc` (×5) | modified | All globs fixed to actual paths; content replaced generic Omnix boilerplate |
| `.obsidian-ai-memory/MEMORY-READ-PROTOCOL.md` | created | Canonical read rules: 9-file order, 3 modes, red flags, startup block |
| `.obsidian-ai-memory/MEMORY-WRITE-PROTOCOL.md` | created | Canonical write rules: triggers, format, git commit procedure, cross-platform guarantee |
| `.obsidian-ai-memory/templates/session-digest.md` | modified | Full CareerOS format with retrieved/written checklists |
| `.obsidian-ai-memory/templates/decision-entry.md` | modified | Options/choice/tradeoffs/review-trigger structure |
| `.obsidian-ai-memory/templates/error-entry.md` | modified | Symptom/root-cause/fix/prevention/regression structure |
| `.obsidian-ai-memory/05-ARCHITECTURE/README.md` | created | System diagram, student+officer data flows, DB schema map, key conventions |
| `.obsidian-ai-memory/06-WORKFLOWS/README.md` | created | 7 step-by-step procedures (endpoint, table, service, bug, Intel bench, digest) |
| `.obsidian-ai-memory/07-LESSONS/debugging-lessons.md` | created | 2 hard-won lessons from this project |
| `.obsidian-ai-memory/02-PROJECTS/vault-index.md` | modified | Full restructure: protocol pointers, all 7 sections, session history table |

### Commands run

```bash
git add -A && git commit  # ×3 commits this session
```

### Verification

- TypeScript (`tsc --noEmit`): N/A — docs-only session, no TS files changed
- Python AST parse: N/A — no Python files changed
- Alembic: N/A

---

## Decisions made

- None new — all decisions from earlier sessions already in `04-DECISIONS/decisions.md`

---

## Errors encountered and fixed

- None in this session

---

## Memory written after session

- [x] This session digest committed to `01-SESSIONS/2026-05-19/`
- [x] `03-ERRORS/error-memory.md` — no update needed (no bugs)
- [x] `04-DECISIONS/decisions.md` — no update needed (no new decisions)
- [ ] `02-PROJECTS/current-state.md` — no state change this session
- [x] `02-PROJECTS/active-goals.md` — Phase 2 now fully complete
- [x] `02-PROJECTS/vault-index.md` — updated with new session

---

## Open risks / blockers

- Week 1 step 3 (Alembic delta migration + role auth + resume parser) not started yet
- No pilot data — demo will use synthetic corpus. Outcome lift framed as next step in pitch.

---

## Next session — top 3 tasks

1. Write Alembic delta migration: add `colleges`, `departments`, `resume_sections`, `resume_evidence`, `job_descriptions`, `scorecards`, `recommendations`, `batches`, `batch_resumes`, `events_audit`, `benchmark_runs` tables to `services/core-api/migrations/versions/`
2. Add `role` claim to JWT token in `services/core-api/app/services/auth.py` + gate routes by `student`/`officer`/`admin` in `services/core-api/app/dependencies.py`
3. Scaffold `services/resume-parser/` with `pdfplumber` + `python-docx` parser, Indian-fresher section extractor, and a fixture corpus of 5 sample resumes in `services/resume-parser/tests/fixtures/`
