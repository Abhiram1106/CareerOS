# 10 — What's Next

Full product vision: `CareerOS_Complete_Documentation.md` (repo root)

Current state: strong backend + scoring foundation. Frontend pages exist but several critical user-facing flows are incomplete.

---

## Priority order

Pick tasks in this order. Each one builds on the previous.

---

## M1 — Settings page: structured profile editor 🔴 IMMEDIATE

**Why first:** Everything else (resume builder, scoring) gets better data once users can enter structured work experience and education.

**What to build:**
The Settings page (`apps/web/app/(app)/settings/page.tsx`) currently shows basic fields. Replace it with a multi-section editor:

- **Work Experience section:** Add/edit/delete entries. Fields: company, title, employment_type, location, start_date, end_date, is_current, bullets (add/remove/reorder)
- **Education section:** Add/edit/delete. Fields: institution, degree, field, start_year, end_year, cgpa
- **Skills section:** Tag-based input with category dropdown. Use `POST /profile/skills/bulk` to replace all on save
- **Projects section:** Add/edit/delete. Fields: title, description, tech_stack (comma-separated), github_url, live_url
- **Certifications section:** Add/edit/delete. Fields: name, issuer, issue_date, credential_url
- **Social links section:** phone, LinkedIn, GitHub, portfolio (single form, `PUT /profile/links`)
- **Profile completeness meter** updates as sections are filled (reads from `/profile/complete`)

**APIs already live:** All 24 endpoints exist (`GET/POST/PUT/DELETE /profile/work-experience` etc.)
**Frontend API wrappers:** All typed in `apps/web/lib/api.ts`

**Files to create/modify:**
- `apps/web/app/(app)/settings/page.tsx` — full rewrite
- `apps/web/hooks/useProfileSections.ts` — new hook to manage all sections state

---

## M2 — Resume builder: read from structured data + 3 templates 🔴 HIGH

**Why:** Resume generator currently reads from flat text blobs. Structured data makes it actually useful.

**What to build:**

**Backend:**
- Update `generate_resume_handler.py` to accept `structured=true` mode
- Read from `WorkExperience`, `Education`, `Skill`, `Project`, `Certification` via `GET /profile/complete`
- 3 template types: `single_column_clean`, `technical_dev`, `fresher_optimised`
- Each template is an HTML/CSS string rendered by WeasyPrint → ATS-safe PDF
- Template rules per doc: no tables for layout, no text boxes, standard fonts, text-selectable

**Frontend:**
- Template gallery in `/resume` page: 3 cards with ATS compatibility badge per template
  - `single_column_clean`: "Maximum ATS Compatibility ⬆️"
  - `technical_dev`: "High ATS Compatibility — developer-focused"
  - `fresher_optimised`: "High ATS Compatibility — emphasises education + projects"
- "Generate from my profile" button → calls `POST /resumes/generate`
- Live text preview of generated content (simple `<pre>` block from `content` field)
- Professional summary auto-generator: short button that calls `POST /resumes/generate` and extracts just the summary

**Files to modify:**
- `services/ai-rewriter/app/modules/rewrite/mutation/generate_resume_handler.py`
- `apps/web/app/(app)/resume/page.tsx`

---

## M3 — Multi-vendor ATS simulation 🔴 HIGH

**Why:** Core differentiator per the product doc. Current ATS scoring is parse-safety only.

**What to build:**

**Per the doc** (FR-ATS-006), simulate these ATS systems weighted by Indian market prevalence:

| ATS | Weight | Key behavior |
|---|---|---|
| Taleo (Oracle) | 18% | Strict section headers, penalises tables |
| Workday | 16% | Strong keyword matching |
| Naukri RMS | 15% | India-specific, handles Indian degree names |
| Greenhouse | 12% | Keyword density focus |
| PeopleStrong | 10% | Indian HR, handles regional names |
| Darwinbox | 9% | Similar to Workday |
| Lever | 8% | Startup parser, lenient on format |

Build as a rule-based vendor engine:
- `services/ats-engine/app/modules/ats/vendors/` — one file per vendor, each returns a dict of dimension scores
- Composite score = weighted average across all vendors
- Keyword gap analysis table: JD keywords vs resume keywords, present/missing
- Score history: `GET /ats/history?resume_id=N` (time-series from scorecards table)

**Frontend:**
- Keyword gap table in `/match` page showing what the user is missing per JD
- ATS score history sparkline on dashboard

---

## M4 — Application tracker UI 🟡 MEDIUM

**Why:** The database table and all 24 APIs are already live. Just needs UI.

**What to build:**
- "Save job" button on each `JobCard` in `/jobs` → `POST /applications`
- `/applications` page: kanban-style columns
  ```
  Saved | Applied | Screening | Interview | Offer / Rejected
  ```
- Each card: job title, company, date saved, linked resume
- Drag-and-drop or dropdown to update status
- "Mark applied" sets `applied_at` automatically (handled server-side)

**Files to create:**
- `apps/web/app/(app)/applications/page.tsx`
- Update `apps/web/components/workspace/JobCard.tsx` to add save button

---

## M5 — Analytics: score history 🟡 MEDIUM

**What to build:**
- Backend: `GET /analytics/ats-history` → array of `{date, overall_score, bucket}` from `scorecards` table
- Dashboard: small sparkline chart showing score trend over time
- "Your score has improved 14 points this week" callout if improvement detected

**Files to modify:**
- Add `analytics_controller.py` in `services/core-api/app/api/controllers/`
- `apps/web/app/(app)/dashboard/page.tsx`

---

## M6 — Guided resume builder wizard 🟡 MEDIUM

**What to build:**
Per FR-RB-001 and FR-RB-002 from the doc:

A multi-step conversational wizard at `/resume/builder`:
1. "What kind of role are you targeting?" → sets `target_role`
2. "Tell me about your most recent internship/job" → populates WorkExperience
3. "What's your tech stack?" → populates Skills
4. AI suggests STAR bullet rewrites for each experience entry using the rewriter

This can be rule-based (no LLM needed) using the existing proof-linked rewriter.

---

## Post-MVP backlog

- LinkedIn OAuth (FR-CP-006) — profile import
- Google OAuth sign-in (EI-003)
- Job alerts + email notifications (FR-JI-005)
- Cover letter generator (Phase 3)
- B2B college portal — `(officer)/` route group, batch upload, dept heatmap
- Recruiter database access module
- ATS engine ML upgrade (XGBoost on outcome data)
- OpenVINO IR model for embeddings (2–3× faster inference)
- Native mobile app (React Native)

---

## Conventions for new work

- Every new API endpoint needs a typed wrapper in `apps/web/lib/api.ts`
- Every scoring change must pass the discrimination gate (5/5)
- Every Python file must AST-parse clean
- Every frontend change must pass `tsc --noEmit`
- Commit vault digest after every significant session: `.obsidian-ai-memory/01-SESSIONS/YYYY-MM-DD/`
- Commit format: `feat:` / `fix:` / `docs:` / `memory:` — one concern per commit
