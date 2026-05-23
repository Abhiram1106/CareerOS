---
tags: [project, goals, week-plan]
type: project
updated: 2026-05-23
links: [MASTER_PLAN, _INDEX, scoring-knowledge]
---

# Active Goals

← [[MASTER_PLAN]] · [[_INDEX]]

> Sorted by week of the 5-week plan
> (`C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md`).

## Week 1 (complete)

- [x] **Phase 1**: archive branch + cut billing/nexus/job-intel/legacy
- [x] **Phase 2**: monorepo skeleton (apps/packages/services/infra/platform/docs/tests) + .claude/ + CODEOWNERS + README + Omnix memory populated
- [x] **W1.3 — Real Alembic delta migration**: add colleges, departments, resume_sections, resume_evidence, job_descriptions, scorecards, recommendations, batches, batch_resumes, events_audit, benchmark_runs.
- [x] **W1.4 — Role-based auth**: add `role` claim to JWT; gate routes by `student` / `officer` / `admin`.
- [x] **W1.5 — Resume upload + parser**: build `services/resume-parser` with pdfplumber + python-docx + section extractor; wire `/resumes/upload` endpoint in core-api; render extracted sections in `apps/web`.

## Week 2 (complete — 2026-05-21)

- [x] JD parser + skill taxonomy + eligibility extractor (`match-engine` + `POST /jd/parse`).
- [x] `services/match-engine`: TF-IDF + char n-gram cosine (embedding proxy) + skill recall + eligibility rule score; sklearnex patch first.
- [x] Narrow `services/ats-engine` to the ATS-Parse-Safety penalty model only (`POST /parse-safety`; core-api `POST /ats/parse-safety`; legacy composite `/scan` removed).
- [x] `packages/scoring/` — Python lib implementing the full [[scoring-knowledge|PlacementReadinessScore]] formula.
- [x] `POST /scorecards/score` in core-api + docker `match-engine` service.
- [x] `apps/web` workspace score breakdown (six bars + bucket + missing/matched skills via `/scorecards/score`).

## Audit hardening (complete — 2026-05-23)

- [x] **P0 RBAC**: `require_student` / `require_officer` on all role-specific routes.
- [x] **P0 Honest labels**: `semantic_method: "embedding_proxy_tfidf"` on match results + UI tooltip.
- [x] **P0 Tests**: golden-path API integration test (`tests/test_scoring_golden_path.py`) + hardened formula unit tests.
- [x] **P1 Persistence**: `ats_flags` and `college_id` (request → user fallback) stored on scorecards.
- [x] **P1 Cleanup**: deleted orphaned legacy UI stack (panes/AppHeader/SiteNav/SectionNav/WorkspaceTabs/AppFooter/useCareerOSWorkspace).

## Week 3 — AI rewriter + export

- [ ] `services/ai-rewriter` retargeted: proof-linked JSON-schema output, system prompt from research §"Guardrails".
- [ ] Before/after diff UI in `apps/web`.
- [ ] ATS-safe PDF export using existing WeasyPrint task.

## Week 4 — Officer dashboard

- [ ] `apps/web/(officer)/` route group: dashboard, batches, jds, review.
- [ ] Batch upload, dept heatmap, review queue, skill-gap chart, company-fit columns.
- [ ] Readiness PDF report export.

## Week 5 — Intel benchmark + pitch

- [ ] `services/intel-bench` harness: OpenVINO + sklearnex measurements.
- [ ] `apps/web/lab/intel` panel rendering measured p50/p95/throughput/accuracy-delta.
- [ ] 6-slide pitch deck in `docs/pitch/`.
- [ ] 3-minute demo script.
- [ ] Top-level README polish + screen captures.

---
_Updated: 2026-05-23 — Week 2 + audit hardening complete; Week 3 (AI rewriter) next._

*Related: [[MASTER_PLAN]] · [[_INDEX]] · [[02-PROJECTS/project-context]] · [[02-PROJECTS/current-state]] · [[scoring-knowledge]] · [[intel-index]] · [[session-index]]*
