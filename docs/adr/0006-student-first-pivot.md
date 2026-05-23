# ADR 0006: Student-First Job Match Agent (Reuse-First)

- Date: 2026-05-23
- Status: Accepted
- Deciders: CareerOS engineering team

## Context

The product objective shifted to a student-first flow with these mandatory capabilities:

1. ATS parser and scorer
2. Resume builder
3. Real-time job fetch
4. JD match percentage and recommender
5. Small in-product AI agent that automates the loop

The repository already had a functioning multi-service pipeline (`resume-parser`, `ats-engine`, `match-engine`, `ai-rewriter`, `packages/scoring`) and recently completed proof-linked rewrites. Rebuilding from scratch would waste prior work and increase regression risk.

## Decision

Adopt a **reuse-first refactor** with a deterministic orchestration agent:

- Keep existing services and integrate them through `core-api` orchestration.
- Add only one new backend service: `services/jobs-feed`.
- Add deterministic state machine in `core-api` (`/agent/run`, `/agent/runs/{id}`).
- Keep officer surface code in repo but gate it behind feature flags:
  - `ENABLE_OFFICER_SURFACE` (core-api)
  - `NEXT_PUBLIC_ENABLE_OFFICER_SURFACE` (web)

## Rationale

- Preserves Week 1-3 implementation value and avoids architectural churn.
- Deterministic agent satisfies "small AI agent" requirement without introducing LLM cost or nondeterminism.
- Keeps Intel story concrete via sklearnex benchmarked match path.
- Reduces delivery risk by reusing validated APIs and UI primitives.

## Consequences

### Positive

- Minimal net-new surface area
- Fast path to integrated demo
- Existing tests remain relevant with additive coverage
- Clear upgrade path to hybrid/LLM agent later (if required)

### Trade-offs

- Agent quality depends on existing rule-based components
- Job feed quality depends on external provider limits and seed fallback
- Officer routes are hidden, not removed (maintenance overhead remains)

## Implementation Notes

- New persistence tables: `jobs`, `agent_runs`
- New benchmark harness: `services/match-engine/bench/run.py` (50x50 stock vs sklearnex)
- New docs:
  - `docs/benchmarks/match-engine-sklearnex.md`
  - `docs/pitch/demo-script.md`

