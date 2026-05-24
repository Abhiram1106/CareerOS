# ADR 0006 — Student-first product scope

## Status

Accepted

## Context

The project previously contained mixed product directions. To reduce complexity and deliver measurable value, the product scope was narrowed to student-only workflows.

## Decision

Adopt a strict student-first scope:

- Keep resume parsing, ATS scoring, JD scoring, rewrite assistance, jobs, export, assistant.
- Remove non-student runtime surfaces and related docs/config.
- Keep architecture focused on direct student outcomes.

## Consequences

- Smaller, more maintainable system
- Clearer roadmap and validation metrics
- Faster onboarding for contributors and evaluators
