---
tags: [decisions, adr, architecture]
type: decision-log
updated: 2026-05-21
links: [_INDEX, architecture-index, 04-DECISIONS/decisions]
---

# Decisions

← [[_INDEX]] · [[architecture-index]]

> Non-trivial choices with rationale. Append-only — supersedes recorded
> by date and `**Status: superseded by ...**` note. Full ADRs live in
> `docs/adr/`; this is the quick-lookup index.

**Graph anchors:** Decision 1 · Decision 2 · Decision 3 · Decision 4 · Decision 5 (headings below)

---

## Decision 1 — Pivot to Campus AI

## 2026-05-19 — Pivot to Campus AI

**Decision**: Reposition CareerOS from a broad "AI for careers" platform
(recruiter pipeline + job board + billing + resume builder) to **CareerOS
Campus AI — an Intel-optimized placement-readiness operating layer for
Indian colleges**. One sharp loop: resume → ATS-safe + JD-matched +
proof-linked scoring → student fixes + officer cohort dashboard → Intel
benchmarks.

**Rationale**: Pre-pivot positioning scores ~6/10 per `deep-research-report.md`
because it competes with Naukri/Internshala/Apna on distribution and student
habit (territory we cannot win). Placement-readiness is institutional pain
with no entrenched competitor, real measurable outcomes, and an honest Intel
story (CPU-bound NLP inference + analytics — where OpenVINO and sklearnex
genuinely shine).

**Status**: Accepted. Full record at `docs/adr/0001-pivot-to-campus-ai.md`.

**Consequences**: Cut NEXUS recruiter side, billing, public job board, job
alerts, application tracker, LinkedIn import. Recoverable via
`origin/archive/pre-campus-ai` branch.

---

## Decision 2 — Hybrid small-team monorepo structure

## 2026-05-19 — Hybrid small-team monorepo structure

**Decision**: Use the small-team variant from
`deep-research-report (1).md`: **`apps/` + `packages/` + `services/` +
`infra/` + `platform/` + `docs/` + `tests/`**, with Omnix integration baked
into `platform/omnix/`. Asset-type grouping (not domain-first).

**Rationale**: Matches the strongest open-source polyglot monorepos at our
scale (Angular, Azure SDK JS, Nx, Rushstack). Domain-first variant is
overkill for one product. Platform layer makes engineering tooling
first-class instead of buried in the first app that needed it.

**Status**: Accepted. Full record at `docs/adr/0002-monorepo-structure.md`.

**Consequences**: pnpm workspaces lock-in for JS side. Python services stay
self-contained. Nx adoption deferred until ≥2 JS apps or ≥3 shared TS
packages. Bazel deferred indefinitely.

---

## Decision 3 — Work on `main` only, no feature branches

## 2026-05-19 — Work on `main` only, no feature branches

**Decision**: Per user direction, all restructure + feature work happens
directly on `main` in this repo folder. No `archive/` or `feature/`
branches for new work; recoverability via `origin/archive/pre-campus-ai`
already covers the pre-pivot rollback path.

**Rationale**: Solo build, fast iteration, single source of truth. Trunk-
based per research §"Google's published guidance".

**Status**: Active.

**Consequences**: Every commit on `main` must leave the tree buildable
(tsc clean, python AST clean). No "WIP" or "broken" commits. Reverting via
`git revert <sha>` if needed.

---

## Decision 4 — Score formula source of truth: `packages/scoring/`

## 2026-05-19 — Score formula source of truth: `packages/scoring/`

**Decision**: The PlacementReadinessScore formula (6 components, JD_Match
sub-formula) lives in `packages/scoring/` as a Python package consumed by
both `services/core-api` (live scoring) and `services/intel-bench`
(benchmark harness).

**Rationale**: Avoids drift between the demo's "score lift" and the
benchmark's "score lift". One implementation, one set of tests, one source
of measurable claims.

**Status**: Decided; implementation lands Week 2.

---

## Decision 5 — Omnix runtime stays at `.omnix/`, committed config target is `platform/omnix/`

## 2026-05-19 — Omnix runtime stays at `.omnix/`, committed config target is `platform/omnix/`

**Decision**: The `.omnix/` directory at repo root remains where Omnix
tooling looks for runtime state (settings/, agents/, workflows/,
commands/, memory/, cache/). The `platform/omnix/` directory exists as the
**intended target** for committed config once Omnix supports a configurable
path. For now, `platform/omnix/README.md` documents the split; canonical
sources live at `.omnix/`.

**Rationale**: Don't fight tooling defaults. Document the intent so the
future migration is straightforward.

**Status**: Active.

---

## Decision 6 — Security-first future phases (Kirito roadmap)

## 2026-05-23 — Security-first future phases (Kirito roadmap)

**Decision**: All Phase 4+ delivery is **gated** on security architecture:
CIA (confidentiality, integrity, availability), JWT + RBAC + ownership
checks, committed OpenAPI, input validation, TLS/secrets in prod, audit
logging, and threat-model updates. Campus assistant (Phase 6) uses RAG +
optional external LLM with proof-linked guardrails; no fabrication in
rewriter paths.

**Rationale**: Intel bootcamp demo must read as production-oriented, not
prototype-only. Officer dashboard and assistant expand attack surface;
security work is parallel requirement, not a later polish pass.

**Status**: Accepted. Vault: `05-ARCHITECTURE/security-architecture.md`.
Repo: `docs/adr/0007-security-first-future-phases.md`.

**Consequences**: Phase 4 officer UI blocked until IDOR tests + OpenAPI
export + rate limits; Phase 6 assistant requires authz on retrieval;
Surf/LLM keys never in git.

---

*Related: [[_INDEX]] · [[architecture-index]] · [[05-ARCHITECTURE/security-architecture]] · [[MASTER_PLAN]]*
