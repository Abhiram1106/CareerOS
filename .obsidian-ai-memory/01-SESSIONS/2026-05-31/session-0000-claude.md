---
date: 2026-05-31
tool: claude-code
model: claude-opus-4-8 → claude-sonnet-4-6
tags: [session, audit, scoring, parser, eligibility, skills, phase1, phase2, phase4]
type: session
links: [error-memory, active-goals, scoring-knowledge, architecture-index]
---

# Session 2026-05-31 — Full-stack fine-tune audit (Phases 0–4)

← [[_INDEX]] · [[error-memory]] · [[active-goals]]

## What was done

### Context
User requested a brutal audit of the full stack: "it's a 2/10 app with false outputs". Full audit → test → rebuild → retest cycle across Phases 0–4.

---

### Phase 0 — Test harness (new)
- Created `tests/golden/corpus.py` — 7 distinct resume personas across strong/mid/weak tiers
- Created `tests/golden/_runner.py` — discrimination gate: asserts every sub-score has ≥30 spread and ≥5 distinct values across the corpus (run inside core-api container)
- Created `tests/golden/_audit_phase4.py` — 21 targeted sub-score correctness tests with expected ranges
- Baseline captured: `interview_readiness` (2 values), `placement_hygiene` (3 values), `profile_completeness` (4 values) — all FAIL → proves the theater

---

### Phase 1 — Data pipeline root-cause fix
**Root bug:** `content_text` was never saved at upload — `analyze_ats` and the match engine received near-empty text → scores clustered regardless of resume quality.

Files changed:
- `services/resume-parser/app/modules/parse/dto/parse_dto.py` — added `full_text: str` to `ParseResponse`
- `services/resume-parser/app/modules/parse/mutation/parse_resume_handler.py` — returns `full_text`, OCR fallback for scanned PDFs (with `len(raw) > 50_000` guard), honest error message replaces "Week 2" stub
- `services/resume-parser/app/parsers.py` — added `ocr_pdf()` using pytesseract + pdf2image; degrades gracefully with specific warnings if Tesseract unavailable
- `services/resume-parser/Dockerfile` — added `tesseract-ocr poppler-utils` APT packages; `pytesseract==0.3.13 pdf2image==1.17.0` in requirements
- `services/resume-parser/app/extractor.py` — third heading signal (alias-matched lines with trailing colon/dash); `header` bucket preserved (not dropped); `_section_confidence()` now derived from match quality + richness (was hardcoded 0.9/0.6); removed `contact_in_header` heuristic (was firing on every normal resume)
- `services/core-api/app/adapter/db/persistence/resume/resume_repo.py` — `create_uploaded()` now accepts `content_text`
- `services/core-api/app/modules/resume/mutation/upload_resume_handler.py` — parse first, then create row with `content_text`; reorder fixes atomicity

Phase 1 bugs found in self-review:
1. OCR triggered on sparse-but-valid PDFs (missing `len(raw) > 50_000` guard)
2. `contact_in_header` heuristic fired on every well-formatted resume (email on line 1 = normal, not a flag)

Verification: DB `content_text` lengths — resume 14: 456 chars, resume 15: 98 chars (was 0 for both).

---

### Phase 2 — Real eligibility + skill synonym matching

**Eligibility:**
- Added `cgpa`, `active_backlogs`, `branch`, `grad_year` to `CareerProfile` entity
- Alembic migration `0002_profile_eligibility_fields.py` (applied directly via ALTER TABLE to running DB)
- `services/core-api/Dockerfile` — now copies `migrations/` + `alembic.ini` (so `alembic upgrade head` works in container)
- `ProfileUpsert` DTO, `ProfileRepo.upsert_for_user`, `UpsertProfileHandler`, `to_profile_response` mapper — all extended with new fields
- `ScoreResumeHandler` — passes new fields to match engine via `profile_dict`
- `services/match-engine/app/matcher.py` — replaced always-100 placeholder with real scoring: CGPA gap penalty (up to -35), backlog penalty (-20/backlog, cap -40), branch mismatch (-15), year mismatch (-20); JD eligibility parsed always (was conditional)
- `services/match-engine/app/main.py` — always parses JD eligibility before calling `compute_match`

Phase 2 bugs found in audit:
1. `"go"` alias → `golang` false positive (common English word)
2. `"cv"` alias → `computer vision` false positive ("CV" = curriculum vitae)
3. `"js"` matched inside `"next.js"` via string substitution → double-match
4. `"c++"` never matched (`\b` fails around `+`)
5. `"ml"` and `"dl"` accidentally removed in false-positive cleanup

All 5 fixed:
- Removed ambiguous single/double-char aliases (`go`, `cv`); restored `ml`, `dl`
- Rewrote `extract_skills_from_text` to use span-claimed longest-match (not string substitution) — aliases skip already-claimed spans
- Fixed `_pattern_for` to use `(?<!\w)..(?!\w)` lookaround for special-char skills

Results: 11/11 alias tests pass, 11/11 eligibility edge cases pass.

---

### Phase 4 — Sub-score rebuilds (replaced theater heuristics)

Replaced all three theater sub-scores in `packages/scoring/careeros_scoring/resume_components.py`:

**`evidence_quality_score`:**
- Was: `45 + verbs×6 + metrics×5` (linear, gameable by repetition)
- Now: 4-signal weighted composite — distinct verb variety (0.30), metric density (0.30), tech-term specificity (0.25), bullet depth median (0.15)
- Key: counts **distinct** action verbs, not occurrences — "built built built" = same as one "built"
- Fixed `_METRIC_RE` — was using `\b` which failed on `40%.` (period after `%`); changed to `(?!\w)` lookahead

**`interview_readiness_score`:**
- Was: 3-bucket step function (40 / 62 / interpolated) on word count
- Now: 5-signal composite — tech density (0.25), metric count (0.25), breadth/has-both-exp-and-projects (0.20), leadership signals (0.15), role variety from date patterns (0.15)

**`placement_hygiene_score`:**
- Was: base 88 with 3 binary penalties → only ~4 possible values
- Now: starts at 100, subtracts for missing contact (email -20, phone -10, links -8), filler phrases (-7/phrase), structural issues (wall-of-text -8, sparse -18), skills specificity graded (0=−10, 1=−5, 6+=+5 bonus)

**`profile_completeness_score`:**
- Was: binary presence check → 6 possible values; empty whitespace counted as "present"
- Now: quality-aware — each section has a minimum word threshold; below threshold = partial credit (0.65), far below = token credit (0.20), whitespace = 0

Phase 4 bugs found in audit: 7
1. `_METRIC_RE` missed `40%.` — period after `%` breaks `\b` word boundary
2-4. Evidence/hygiene/completeness multipliers miscalibrated (too stingy) — recalibrated
5. Hygiene word-count penalty fired on valid short test sections (threshold 80 → lowered to 25)
6. Completeness `< min_wc // 2` threshold too aggressive for real content
7. Skills grading boundary caused regression when 3 tech terms penalised incorrectly

**Final gate results:**
- Discrimination gate: **5/5 PASS** (was 2/5)
- Phase 4 audit: **21/21 PASS**
- `ats_parse_safety`: 7 distinct values, spread 58.9
- `evidence_quality`: 5 distinct values, spread 100.0
- `interview_readiness`: 5 distinct values, spread 89.5
- `placement_hygiene`: 5 distinct values, spread 66.0
- `profile_completeness`: 5 distinct values, spread 93.5

---

## Bugs fixed total: 14 across phases 1-4

## Files changed (code)
- `packages/scoring/careeros_scoring/resume_components.py` — full rewrite of 3 sub-scorers
- `services/resume-parser/app/parsers.py`, `extractor.py`, `parse_dto.py`, `parse_resume_handler.py`, `Dockerfile`, `requirements.txt`
- `services/core-api/app/models/entities.py`, `migrations/versions/0002_*.py`, `Dockerfile`
- `services/core-api/app/adapter/db/persistence/profile/profile_repo.py`
- `services/core-api/app/modules/profile/dto/profile_dto.py`, `mapper/profile_mapper.py`, `mutation/upsert_profile_handler.py`
- `services/core-api/app/modules/scorecard/mutation/score_resume_handler.py`
- `services/match-engine/app/matcher.py`, `main.py`, `skill_taxonomy.py`
- `tests/golden/corpus.py`, `_runner.py`, `_audit_phase4.py`, `test_discrimination.py`, `__init__.py`, `run_in_container.sh`

## Files changed (vault)
- `.obsidian-ai-memory/01-SESSIONS/2026-05-31/session-0000-claude.md` ← this file
- `.obsidian-ai-memory/03-ERRORS/error-memory.md` — appended 6 new entries

---

*Related: [[error-memory]] · [[active-goals]] · [[scoring-knowledge]] · [[architecture-index]]*
