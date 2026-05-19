# Active Goals

> Sorted by week of the 5-week plan
> (`C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md`).

## In progress (Week 1)

- [x] **Phase 1**: archive branch + cut billing/nexus/job-intel/legacy
- [x] **Phase 2**: monorepo skeleton (apps/packages/services/infra/platform/docs/tests) + .claude/ + CODEOWNERS + README + Omnix memory populated
- [ ] **W1.3 — Real Alembic delta migration**: add colleges, departments, resume_sections, resume_evidence, job_descriptions, scorecards, recommendations, batches, batch_resumes, events_audit, benchmark_runs.
- [ ] **W1.4 — Role-based auth**: add `role` claim to JWT; gate routes by `student` / `officer` / `admin`.
- [ ] **W1.5 — Resume upload + parser**: build `services/resume-parser` with pdfplumber + python-docx + spaCy section extractor; wire `/resumes/parse` endpoint in core-api; render extracted sections in `apps/web/(student)/resume/`.

## Up next (Week 2)

- [ ] JD parser + skill taxonomy + eligibility extractor.
- [ ] `services/match-engine`: TF-IDF cosine + sentence-transformer embedding cosine + skill recall + eligibility rule score.
- [ ] Narrow `services/ats-engine` to the ATS-Parse-Safety penalty model only (drop the 5-component composite).
- [ ] `packages/scoring/` — Python lib implementing the full PlacementReadinessScore formula.
- [ ] `apps/web` score breakdown UI (six bars + bucket label + missing skills list).

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
_Updated: 2026-05-19 — Phase 2 complete; Week 1 step 3 next._
