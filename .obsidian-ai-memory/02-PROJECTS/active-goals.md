---
tags: [project, goals, roadmap, careeros]
type: project
updated: 2026-06-02
links: [MASTER_PLAN, _INDEX, scoring-knowledge, security-architecture]
---

# Active Goals — CareerOS Campus AI

← [[MASTER_PLAN]] · [[_INDEX]]

> **Product vision (from CareerOS_Complete_Documentation.md):**
> A unified career intelligence platform: AI-powered resume building, proprietary ATS scoring engine,
> and job intelligence layer — all powered by a single persistent career profile.
> Primary market: Indian students, freshers, early-career professionals.

---

## ✅ Completed (Phases 0–7 + doc-aligned foundation)

### Bootcamp submission phases (Phases 0–7)
- [x] Phase 0 — Test harness + discrimination gate (5/5 PASS)
- [x] Phase 1 — content_text persistence, section extractor hardening, OCR fallback
- [x] Phase 2 — Real eligibility scoring (CGPA/backlogs/branch/grad_year), skill synonyms (70 skills, 50 aliases)
- [x] Phase 3 — MiniLM sentence embeddings (all-MiniLM-L6-v2, 24ms p50, 148K pairs/hr)
- [x] Phase 4 — Content-aware sub-scorers (evidence, interview_readiness, placement_hygiene, profile_completeness)
- [x] Phase 5 — Proof-linked rewriter rebuilt (STAR verb upgrade, filler removal, anti-fabrication)
- [x] Phase 6 — Frontend honesty (hasExport live, dead bell removed, honest formula labels)
- [x] Phase 7 — CI workflow fixed, password reset (console-mode), Intel benchmark docs

### Doc-aligned foundation (latest session)
- [x] Structured career profile entities: WorkExperience, Education, Skill, Project, Certification, JobApplication
- [x] User extended with: phone, linkedin_url, github_url, portfolio_url
- [x] 24 REST endpoints (full CRUD for all section types)
- [x] GET /profile/complete — full structured profile in one call
- [x] Typed API wrappers in apps/web/lib/api.ts
- [x] Alembic migration 0003_structured_profile
- [x] docs/handoff/ — full knowledge-transfer for teammates

---

## 🔴 Next: MVP build (mapped to CareerOS_Complete_Documentation.md)

### M1 — Settings page: structured profile editor ✅ DONE
- [x] WorkSection: add/delete, up to 8 bullets per entry
- [x] EducationSection: institution/degree/field/years/CGPA
- [x] SkillsSection: tag chips with category + proficiency, bulk replace
- [x] ProjectsSection: tech stack array, GitHub/live URLs
- [x] CertificationsSection: name/issuer/date/credential URL
- [x] LinksSection: phone, LinkedIn, GitHub, portfolio
- [x] CompletenessRing: SVG progress + 5-item live checklist
- [x] `useProfileSections.ts` hook: per-action saving state, auto-reload

### M2 — Resume builder: read from structured profile (HIGH)
> FR-RB-001 to FR-RB-010 from the doc.
- [ ] Resume generator reads WorkExperience, Education, Skills, Projects from structured DB
- [ ] 3 ATS-safe templates: single-column-clean, technical-dev, fresher-optimised
- [ ] Template HTML/CSS rendered by WeasyPrint → ATS-safe PDF
- [ ] Template selector UI in `/resume` page with ATS compatibility badge per template
- [ ] Live text preview (rendered from structured profile)
- [ ] Professional summary auto-generator from target_role + skills + experience
- **Files to touch:** `services/ai-rewriter/app/modules/rewrite/mutation/generate_resume_handler.py`, `apps/web/app/(app)/resume/page.tsx`

### M3 — Multi-vendor ATS simulation (HIGH)
> FR-ATS-006: simulate Taleo, Workday, Naukri RMS, Greenhouse, PeopleStrong, Darwinbox, Lever.
- [ ] ATS vendor rule engine: per-vendor weight map + parsing quirks
- [ ] Composite score = weighted average across simulated vendors
- [ ] Keyword gap analysis: JD keywords vs resume, missing + present table
- [ ] Score history endpoint: GET /ats/history?resume_id=N (time-series)
- [ ] Radar chart data in scorecard response
- **Files to touch:** `services/ats-engine/app/`, new vendor rule files

### M4 — Application tracker UI (MEDIUM)
> FR-JI-006: per-job save/track workflow.
- [ ] "Save job" button on JobCard → POST /applications
- [ ] `/applications` page: kanban columns (saved → applied → screening → interview → offer/rejected)
- [ ] Status update via drag or dropdown
- [ ] Resume version linked to each application
- **Files to touch:** `apps/web/app/(app)/jobs/page.tsx`, new `apps/web/app/(app)/applications/page.tsx`

### M5 — Analytics: score history + skill trends (MEDIUM)
> FR-AD-001, FR-AD-002.
- [ ] GET /analytics/ats-history: scorecard scores over time (date + overall_score)
- [ ] Dashboard score trend mini-chart (sparkline)
- [ ] Skill demand signal: which JD skills appear most in user's scans
- **Files to touch:** `services/core-api/app/api/controllers/` new analytics controller, dashboard page

### M6 — AI resume builder: guided mode (MEDIUM)
> FR-RB-001, FR-RB-002, FR-RB-003.
- [ ] Conversational wizard: profile status → role → skills → experience bullets
- [ ] STAR bullet suggestions per internship/experience entry
- [ ] AI uses profile sections + target_role to generate context-aware content
- [ ] No LLM required — rule-based STAR template is acceptable for MVP
- **Files to touch:** `apps/web/app/(app)/resume/builder/page.tsx` (new), `services/ai-rewriter/`

---

## 🟡 Post-MVP (Phase 3 in the doc)

- [ ] B2B college portal (placement officer dashboard) — separate route group `(officer)/`
- [ ] Recruiter database access module
- [ ] LinkedIn OAuth for profile import (FR-CP-006)
- [ ] Google OAuth sign-in (EI-003)
- [ ] Job alerts + email notifications (FR-JI-005)
- [ ] Cover letter generator
- [ ] LinkedIn profile optimizer
- [ ] Native mobile app (React Native)
- [ ] ATS engine ML upgrade (XGBoost on scan outcome data)
- [ ] OpenVINO IR model for embedding inference (OPENVINO_MODEL_DIR)

---

## Cross-cutting — always in scope

- [ ] RBAC on every new endpoint (`require_student`)
- [ ] No secrets in git; `.env.example` placeholders only
- [ ] PlacementReadinessScore only in `packages/scoring/`
- [ ] No fabrication in rewriter (`unsupported_claims[]`)
- [ ] tsc --noEmit clean before every commit
- [ ] Python AST-parse clean on all touched services
- [ ] Discrimination gate 5/5 before any scoring change

---

_Updated: 2026-06-02 — Goals realigned to CareerOS_Complete_Documentation.md full product vision._

*Related: [[MASTER_PLAN]] · [[_INDEX]] · [[scoring-knowledge]] · [[05-ARCHITECTURE/security-architecture]]*
