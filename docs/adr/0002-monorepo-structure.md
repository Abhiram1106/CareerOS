# ADR 0002 — Monorepo structure

## Status

Accepted

## Context

CareerOS uses multiple services and packages that share contracts and scoring logic.

## Decision

Maintain a monorepo with clear boundaries:

- `apps/` for deployable UIs
- `services/` for backend/runtime services
- `packages/` for shared logic and contracts
- `docs/` for architecture, ADRs, security, and deployment

## Consequences

- Easier cross-service refactors
- Single source of truth for shared scoring logic
- Requires discipline on module boundaries and dependency hygiene
