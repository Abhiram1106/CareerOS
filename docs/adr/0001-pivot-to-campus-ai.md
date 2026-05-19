# ADR 0001 — Pivot to Campus AI (placement-readiness platform)

- **Status**: Accepted
- **Date**: 2026-05-19
- **Deciders**: Abhiram Jonnadula (project owner)
- **Supersedes**: pre-pivot CareerOS positioning (see `docs/legacy/v0-careeros-docs/`)

## Context

CareerOS was originally positioned as a broad "AI for careers" platform with a
recruiter pipeline (NEXUS), public job board, paid billing (Stripe + Razorpay),
job alerts, application tracker, and resume builder. For the Intel bootcamp
submission, two pieces of research (`deep-research-report.md`,
`deep-research-report (1).md`) and the brutal upgrade direction concluded that
this positioning scores ~6/10 because it competes with Naukri/Internshala/Apna
on distribution and student habit — territory we cannot win.

## Decision

Reposition as **CareerOS Campus AI — an Intel-optimized placement-readiness
operating layer for Indian colleges**. One sharp workflow:

1. Students upload resumes → real PDF/DOCX parsing → structured JSON.
2. Hybrid match against a pasted JD (TF-IDF + sentence embeddings + skill
   recall + eligibility) → six-component **PlacementReadinessScore**.
3. Proof-linked AI rewriter (no fabrication) → ATS-safe PDF export.
4. Placement-officer dashboard: cohort readiness, review queue, skill-gap
   heatmap, department breakdown, readiness PDF report.
5. Intel benchmark lab: OpenVINO + sklearnex measured speedups on real
   workloads (no marketing claims, real numbers only).

## Consequences

### What we get
- A focused 9+/10 bootcamp project per research scorecard.
- Institutional buyer (placement cells), real measurable pain.
- Honest Intel story (CPU-bound NLP inference + analytics — exactly where
  OpenVINO and sklearnex shine).
- Demoable in 3 minutes: dashboard → low-score student → rewrite refusal of
  unsupported claims → score lift → Intel benchmark panel.

### What we give up
- Recruiter side / NEXUS ATS hiring pipeline.
- Billing infrastructure (Stripe + Razorpay).
- Public job board, scraping, LinkedIn import (research §"LinkedIn and
  external API risk" — terms-sensitive, anti-pattern).
- Job alerts + application tracker.
- "Big platform" framing.

### Risks accepted
- No real pilot data in 5 weeks — demo runs on synthetic + small hand-labeled
  cohort. Outcome lift framed as the *next* step with event-logging plumbing
  already in place.
- PDF parsing fragility on Indian fresher resumes (Canva templates, two-column,
  scanned). Mitigated by a checked-in fixture corpus.
- DPDP compliance is design-level only (RBAC + audit logs + retention hooks);
  no legal review.

## Implementation

See the plan file at `C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md`
and the five-week roadmap there. Phase 1 (cut + restructure) landed in commits
`c327416` + `172160a`. Phase 2 (monorepo skeleton + .claude + Omnix memory)
follows.

## References

- `deep-research-report.md` — competitive landscape, scoring formula, MVP plan
- `deep-research-report (1).md` — monorepo structure research (hybrid variant
  selected)
- Brutal upgrade direction (in conversation, 2026-05-19)
