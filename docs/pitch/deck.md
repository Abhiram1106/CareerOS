# CareerOS Campus AI — 6-slide pitch deck (markdown)

> Export to PDF/slides for judges. Screenshots: `docs/pitch/screenshots/`.

---

## Slide 1 — Problem

Indian colleges run campus drives with hundreds of resumes, one JD, and one TPO.

- Students guess formatting and keywords
- Officers lack cohort-level readiness before day-one interviews
- Generic AI rewriters invent claims recruiters reject

---

## Slide 2 — Solution

**CareerOS Campus AI** — placement-readiness operating layer (not a job board).

- Parse → score vs JD → proof-linked rewrite → export
- Officer cohort dashboard + batch intake
- Intel-optimized matching path (measured sklearnex benchmarks)

---

## Slide 3 — Demo loop (student)

1. Upload resume (PDF/DOCX)
2. Paste JD → placement readiness score
3. Proof-linked rewrite with `unsupported_claims[]`
4. Jobs + deterministic agent → PDF export

Campus Assistant: FAQ-grounded guidance (no fabrication).

---

## Slide 4 — Demo loop (officer)

- Cohort KPIs + readiness buckets (live scorecards)
- Department heatmap + top skill gaps
- Batch create + bulk resume upload
- Review queue sorted by score

---

## Slide 5 — Intel optimization

- `services/intel-bench` harness — TF-IDF/sklearnex measured on lab hardware
- `/lab/intel` panel — p50/p95/speedup from `GET /benchmarks`
- OpenVINO embedding path: probe + export step documented (run on Python 3.11/3.12)

Honest skips when packages unavailable — no vendor headline numbers.

---

## Slide 6 — Ask / traction

- Pilot with one college TPO before next drive
- Measured benchmark artifact in repo (`docs/benchmarks/`)
- Security: JWT RBAC, IDOR tests, rate limits, audit log, CI dependency + secrets scan

**Contact:** Bootcamp demo · `docs/pitch/demo-script.md`
