---
tags: [errors, bugs, append-only]
type: error-log
updated: 2026-05-21
links: [errors-index, 03-ERRORS/anti-patterns]
---

# Error Memory

← [[errors-index]] · [[03-ERRORS/anti-patterns]]

> Log fixed bugs and how. Check this before diagnosing anything.

---

## 2026-05-19 — `git mv` + post-rename Edit lost in single commit

**Symptom**: After `git mv frontend/ apps/web/` followed by `Write`/`Edit` to
the moved files, the resulting commit captured only the renames — the content
edits were absent because they weren't re-staged before `git commit`. Git
showed the commit as `+0 -0` net change on edited paths.

**Root cause**: `git mv` stages the rename. Subsequent `Write`/`Edit`
modifies the working tree but does NOT auto-stage the change. `git commit`
without an explicit `git add -u` only commits what's in the index, which at
that point is the *original* content under the new path.

**Fix**: After post-rename edits, `git add -u` (or `git add <paths>`)
**before** `git commit`. Verified by `git show HEAD -- <path>` showing the
intended diff.

**Prevention**: see [[03-ERRORS/anti-patterns#Don't commit after `git mv` + edit without re-staging]].

---

*Related: [[errors-index]] · [[03-ERRORS/anti-patterns]] · [[07-LESSONS/debugging-lessons]] · [[06-WORKFLOWS/README#Fixing a bug]]*

---

## 2026-05-31 — `content_text` never persisted at upload (root-cause data bug)

**Symptom**: ATS scores and match scores clustered regardless of resume quality. Same output for very different resumes.

**Root cause**: `upload_resume_handler.py` called `create_uploaded(user_id, source_format)` before parsing, then only saved sections. `content_text` was never stored. Downstream `analyze_ats` and `compute_match` received near-empty reconstructed text from thin sections.

**Fix**: Parse first, then create the resume row passing `content_text=parse_result["full_text"]`. Also added `full_text` to `ParseResponse` DTO and returned it from `parse_resume_handler`.

**Files**: `upload_resume_handler.py`, `parse_dto.py`, `parse_resume_handler.py`, `resume_repo.py`

---

## 2026-05-31 — OCR triggered on sparse-but-valid PDFs

**Symptom**: Small legitimate PDFs with short text unnecessarily triggered OCR, adding latency and noise.

**Root cause**: OCR condition was `len(text.strip()) < 200` with no file-size guard. A 10 KB sparse-but-valid PDF met the condition.

**Fix**: Added `and len(raw) > 50_000` guard — mirrors the heuristic in `extract_pdf`. Only large files with little extracted text are treated as scanned.

**File**: `parse_resume_handler.py`

---

## 2026-05-31 — `contact_in_header` ATS flag fired on every normal resume

**Symptom**: Well-formatted resumes incorrectly received a `-10` ATS penalty for "contact in header".

**Root cause**: Heuristic checked `if email in first 2 lines AND not in body` — fires for every resume where the email is at the top, which is all of them.

**Fix**: Removed the unreliable text-based detection entirely. The flag still exists in `FLAG_PENALTIES` for callers with real PDF header metadata; it just no longer auto-generates from plain text.

**File**: `extractor.py`

---

## 2026-05-31 — Alias `"go"` matched natural language "go"

**Symptom**: Resume text like "let me go to the store" triggered `golang` in skill extraction.

**Root cause**: `"go": "golang"` alias in `SKILL_ALIASES` used `\bgo\b` which matches any standalone word "go" in prose.

**Fix**: Removed the alias. `golang` is matched directly in `SKILL_TAXONOMY` — only when the full word "golang" appears.

**File**: `skill_taxonomy.py`

---

## 2026-05-31 — Alias `"cv"` matched "curriculum vitae" abbreviation

**Symptom**: "cv of rahul sharma" (i.e., a resume header) triggered `computer vision` skill.

**Root cause**: `"cv": "computer vision"` in `SKILL_ALIASES`. "CV" is universally used as abbreviation for curriculum vitae.

**Fix**: Removed the alias. `computer vision` only matches via direct two-word taxonomy hit.

**File**: `skill_taxonomy.py`

---

## 2026-05-31 — `"js"` alias matched inside `"next.js"` via string substitution

**Symptom**: "built using next.js" produced both `next.js` AND `javascript` as matched skills.

**Root cause**: Alias resolution was implemented as string substitution (`resolved = pattern.sub(canonical, resolved)`). The `js` pattern fired inside `next.js`, corrupting the resolved text before taxonomy scan.

**Fix**: Rewrote `extract_skills_from_text` to use span-claimed longest-match. Pass 1 scans taxonomy (longest-first) and records claimed character spans. Pass 2 scans aliases; any alias match whose span is within a claimed region is skipped.

**File**: `skill_taxonomy.py`

---

## 2026-05-31 — `"c++"` never matched (`\b` fails around `+`)

**Symptom**: Resumes mentioning "C++" never had the skill extracted.

**Root cause**: `_pattern_for("c++")` produced `\bc\+\+\b`. `\b` is a zero-width assertion between a word char and a non-word char. `+` is non-word, so `\b` at the end of `c++` requires a word char after the last `+` — which rarely exists.

**Fix**: `_pattern_for` now uses `(?<!\w)..(?!\w)` lookaround instead of `\b` when the skill contains non-word characters at start or end. Covers `c++`, `c#`, `.net`, `ci/cd`.

**File**: `skill_taxonomy.py`

---

## 2026-05-31 — `_METRIC_RE` missed percentage values followed by `.` (e.g. `40%.`)

**Symptom**: Strong resume bullets with "reduced latency by 40%." produced zero metric matches because the trailing period broke the pattern.

**Root cause**: Metric regex ended with `\b`. After `%`, `\b` requires a word character next — `.` is not a word char, so the word boundary failed.

**Fix**: Changed trailing `\b` to `(?!\w)` negative lookahead — matches when not followed by a word character. Handles `40%.`, `40% `, `40%,` all correctly.

**File**: `packages/scoring/careeros_scoring/resume_components.py`

---

## 2026-05-31 — Sub-score multipliers under-calibrated (evidence/interview/hygiene)

**Symptom**: `evidence_quality` scored 26 for a strong STAR-structured resume with 5 verbs, 4 metrics, 3 tech terms, 7-word median bullets.

**Root cause**: Initial multipliers (`verbs×8`, `tech×7`, depth `×5`) too low. Composite topped out well below expected range for strong content.

**Fix**: Recalibrated — `verbs×10`, `tech×10`, depth `×10`; adjusted weights to 0.30/0.30/0.25/0.15. Also lowered hygiene word-count penalty threshold from 80 → 25 words (was firing on valid concise section subsets) and lowered completeness min-word thresholds to match real resume content.
