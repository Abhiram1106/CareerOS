# ADR 0007 — Security-first future phases

## Status

Accepted

## Context

CareerOS handles sensitive student career data (resume content, scores, recommendations, exports). Future phases must maintain strict confidentiality, integrity, and availability controls.

## Decision

All feature work must pass explicit security gates:

1. Strict request/response contracts
2. Ownership checks on all user-linked resources
3. Auditable event logging for high-impact actions
4. Rate limits on expensive endpoints
5. Assistant safety controls for prompt and output handling

## Consequences

- Slower feature rollout, higher confidence in production behavior
- Clear compliance and operations trail
