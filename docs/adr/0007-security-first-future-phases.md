# ADR 0007: Security-First Future Phases (Kirito Roadmap)

- Date: 2026-05-23
- Status: Accepted
- Deciders: CareerOS engineering team

## Context

CareerOS Campus AI is presented as a production-oriented Intel bootcamp project handling sensitive student career data (resumes, scores, rewrites). Future work includes officer dashboards, Intel lab UI, and an in-product assistant. Stakeholders require every future phase to explicitly address confidentiality, integrity, and availability, with enterprise-grade auth, API validation, encryption in transit, and scalable secure architecture.

Planning work is captured in `.obsidian-ai-memory/05-ARCHITECTURE/security-architecture.md` (vault name: **Kirito roadmap**).

## Decision

1. **Security is a phase gate**, not an optional follow-up. Phases 4–7 each ship product features only together with listed security deliverables.
2. **OpenAPI/Swagger** — maintain FastAPI-generated docs; commit exported OpenAPI under `packages/contracts/openapi/` and keep JSON Schema aligned.
3. **AuthN/AuthZ** — continue JWT + RBAC; extend with resource ownership checks, audit logging, rate limits, and production session hardening before officer GA.
4. **DI pattern** — standardize FastAPI `Depends()` factories for handlers and DB access to improve testability (Python equivalent of autowiring).
5. **Assistant (Phase 6)** — scoped guidance chatbot with RAG over public docs and user-owned context only; external LLM keys server-side; optional TensorFlow/embeddings for retrieval index; no cross-tenant data in prompts.
6. **Internal agent tooling** (e.g. Surf-like dev agents) — dev workflow only unless separately hardened; not student-facing without full security review.

## Consequences

### Positive

- Judges and faculty can evaluate security depth alongside Intel performance story.
- Agents have a single checklist for every future PR.
- Clear path from demo JWT to production TLS and secrets management.

### Trade-offs

- Slower feature velocity until Phase 4 security baseline closes.
- Assistant phase requires privacy disclosure if using third-party LLMs.
- OpenAPI export adds CI maintenance.

## Implementation references

- Vault: `.obsidian-ai-memory/05-ARCHITECTURE/security-architecture.md`
- Goals: `.obsidian-ai-memory/02-PROJECTS/active-goals.md` (Phases 4–7)
- README roadmap section links to ADR 0007
