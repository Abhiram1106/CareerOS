# Session — Week 1 implementation: Alembic migration + role auth + resume parser

Date: 2026-05-20 ~00:01 IST | Tool: claude | Type: feature-build
Week goal: W1.3 Alembic delta migration + W1.4 role auth + W1.5 resume upload + parser

---

## Memory retrieved at session start

- [x] `02-PROJECTS/project-context.md`
- [x] `02-PROJECTS/active-goals.md`
- [x] `03-ERRORS/error-memory.md`
- [ ] `02-PROJECTS/vault-index.md` — skipped (budget)
- [ ] `03-ERRORS/anti-patterns.md` — skipped
- [ ] `04-DECISIONS/decisions.md` — N/A (feature session)
- [ ] `01-SESSIONS/` last 3 — read via context continuity

Known errors at session start: 1 (git mv staging trap — not relevant this session)

---

## Work done

### Files changed

| File | Change | Summary |
|---|---|---|
| `services/core-api/migrations/versions/0002_campus_ai_schema.py` | created | 11 new tables + role column on users |
| `services/core-api/app/models/entities.py` | modified | Full rewrite — all 13 models including 11 new ones |
| `services/core-api/app/services/auth.py` | modified | role claim in JWT, decode_token(), dev fallback carries role |
| `services/core-api/app/dependencies.py` | modified | require_student/officer/admin gates added |
| `services/core-api/app/schemas/contracts.py` | modified | role in RegisterRequest + AuthResponse; ParseResumeResponse added |
| `services/core-api/app/services/clients.py` | modified | parse_resume_file() multipart POST helper |
| `services/core-api/app/config.py` | modified | RESUME_PARSER_URL added |
| `services/core-api/app/main.py` | modified | POST /resumes/upload + GET /resumes/{id}/sections; role in auth responses |
| `services/resume-parser/` (4 files) | created | Full new service: parsers.py, extractor.py, main.py, requirements.txt, Dockerfile |
| `services/resume-parser/tests/fixtures/README.md` | created | Fixture corpus spec |
| `docker-compose.yml` | modified | resume-parser service added |
| `.env.example` | modified | RESUME_PARSER_URL added |
| `apps/web/lib/api.ts` | modified | uploadResume(), getResumeSections(), role in AuthResponse |
| `apps/web/components/panes/types.ts` | modified | ResumeSection, ParseResult types |
| `apps/web/hooks/useCareerOSWorkspace.ts` | modified | onUploadResume, uploading, parseResult state |
| `apps/web/components/panes/ResumePane.tsx` | modified | Upload card + section viewer (accessible labels, CSS classes) |
| `apps/web/app/globals.css` | modified | 10 new CSS classes for parse result UI |

### Commands run

```bash
tsc --noEmit              # TypeScript verification
python -c "ast.parse..."  # Python AST verification
alembic upgrade head      # Migration cycle on fresh SQLite
alembic downgrade base
alembic upgrade head
git add -A && git commit
```

### Verification

- TypeScript (`tsc --noEmit`): **passed**
- Python AST parse (services/core-api, ats-engine, ai-rewriter, resume-parser): **passed**
- Alembic upgrade + downgrade + upgrade on clean DB: **passed**
- Lint error fixed: unlabelled file input → proper `<label htmlFor>` + `id` on input

---

## Decisions made

- `resume_sections.content_json` stored as `Text` (not `JSONB`) for SQLite/Postgres compat during dev. Will migrate to `JSONB` on Postgres in Week 2 when we add indexing on skills. Decision: defer.
- ATS flag detection is deterministic rules (not ML). Consistent with plan §"ATS-parse safety heuristics" — same class of check that real ATS systems fail on.
- File input labelled with `<label htmlFor>` pattern to satisfy accessibility rules in `.cursor/rules/frontend.mdc`.

---

## Errors encountered and fixed

**Error**: `ResumePane.tsx` unlabelled file input — IDE error "Form elements must have labels".
**Fix**: Added `<label htmlFor="resume-file-input">` wrapping the button, added matching `id="resume-file-input"` + `aria-label` on the hidden input.
**Prevention rule**: Hidden inputs that are triggered via a button must still have an explicit `id` + matching `<label>` or `aria-label`.

---

## Memory written after session

- [x] This session digest committed to `01-SESSIONS/2026-05-20/`
- [ ] `03-ERRORS/error-memory.md` — the unlabelled input fix is minor; not adding to error-memory (no root cause investigation needed)
- [ ] `04-DECISIONS/decisions.md` — no new architectural decisions
- [x] `02-PROJECTS/active-goals.md` — W1.3, W1.4, W1.5 checkboxes to mark complete
- [x] `02-PROJECTS/vault-index.md` — session table updated

---

## Open risks / blockers

- **resume-parser is a stub without real fixture corpus.** Parsing accuracy against Indian fresher Canva templates unknown until we add fixtures in `services/resume-parser/tests/fixtures/`. This is the #1 risk for Week 2 demo.
- **pdfplumber + python-docx not yet installed locally** — `docker compose up --build` required before testing end-to-end.
- **`resume_sections.content_json` is stored as raw `Text`** — no Postgres JSONB indexing yet. Skills extraction from the JSON is in Week 2.
- **`require_student`/`require_officer` gates not yet applied to any routes** — all protected routes still use `current_user` only. Gating lands with officer dashboard (Week 4).

---

## Next session — top 3 tasks

1. **Week 2 — JD parser**: Build `/jd/parse` endpoint in core-api that extracts `required_skills`, `nice_to_have_skills`, `eligibility` (cgpa, branches, backlogs) from pasted JD text using a skill taxonomy dictionary + regex rules.
2. **Week 2 — Match engine service**: Scaffold `services/match-engine/` — TF-IDF cosine (sklearnex) + sentence-transformer embedding cosine + skill recall + eligibility rule score → returns the 4-component JD_Match breakdown.
3. **Week 2 — Score breakdown UI**: `apps/web` — add a JD paste input in the Resume pane, trigger match-engine via core-api, render the 6-bar PlacementReadinessScore breakdown with bucket label and missing-skills list.
