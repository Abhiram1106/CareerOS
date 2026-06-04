---
date: 2026-06-02
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M2, resume-builder, templates, cleanup, repo-organisation]
type: session
links: [error-memory, active-goals]
---

# Session 2026-06-02 (4) — Repo cleanup + M2 resume builder

## Repo cleanup

Dissolved hollow folders with no real code:

| Deleted | Moved to |
|---|---|
| `.omnix/` (READMEs + settings JSON only) | — |
| `platform/` (pointed to .omnix/) | — |
| `infra/seed/jobs.seed.json` | `services/jobs-feed/seed/jobs.seed.json` |
| `scripts/run-intel-bench-py312.ps1` | `services/intel-bench/run-py312.ps1` |
| `.cursorrules` (subset of .cursor/AGENTS.md) | — |

Updated `docker-compose.yml` seed volume mount and `jobs-feed/app/main.py` default path.
Verified: 10 seed jobs load from new location.
README.md rewritten to reflect clean structure.

---

## M2 — Resume builder reads structured profile

### Backend

**`services/ai-rewriter/app/modules/rewrite/mutation/generate_resume_handler.py`** (full rewrite):
- 3 template renderers:
  - `classic`: Education → Experience → Projects → Skills (max ATS compat)
  - `technical`: Skills first, GitHub in contact header, Projects → Education
  - `fresher`: Education first, Projects before Experience
- All read from structured tables: WorkExperience bullets (JSON array), Education CGPA/field,
  Skills by category, Projects tech_stack, Certifications with credential_url
- Contact header populated from user.phone/linkedin_url/github_url/email
- `[Bracketed placeholders]` only when sections are empty — never silent boilerplate

**`services/ai-rewriter/app/modules/rewrite/dto/resume_prompt_dto.py`**:
- Added `ResumeStructuredPrompt(template_name, profile_data: dict)`
- `ResumePrompt` kept for backward compat

**`services/ai-rewriter/app/api/controllers/rewrite_controller.py`**:
- `POST /generate/from-profile` — new structured endpoint
- `POST /generate/resume` — legacy kept, wraps internally

**`services/core-api/app/services/clients.py`**:
- `generate_resume_from_profile(template_name, profile_data)` added

**`services/core-api/app/modules/resume/mutation/generate_resume_handler.py`** (full rewrite):
- Loads WorkExpRepo, EducationRepo, SkillRepo, ProjectRepo, CertificationRepo
- Assembles full `profile_data` dict from all structured tables
- Calls `generate_resume_from_profile` instead of old flat-field endpoint

### Frontend

**`apps/web/app/(app)/resume/page.tsx`** (rebuilt):
- Template gallery: 3 cards with ATS badge + description
- Selected template highlighted with blue border + checkmark
- Scrollable text preview of generated content
- Export section preserved

### Verified
- All 3 templates generate from real structured data in DB
- `tsc --noEmit` clean
- DB content correct UTF-8 (PowerShell console encoding artifact only)

---

## What's next: M3 — Multi-vendor ATS simulation

Current ATS scoring is parse-safety only (7-dimension text analyzer).
M3 adds vendor-specific rule simulation: Taleo, Workday, Naukri RMS, Greenhouse, PeopleStrong.
Composite score = weighted average across vendors.
Also: keyword gap analysis table (JD keywords vs resume, present/missing).

_Related: [[active-goals]] · [[error-memory]]_
