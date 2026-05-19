# ADR 0002 — Hybrid monorepo structure (apps + packages + services + infra + platform)

- **Status**: Accepted
- **Date**: 2026-05-19
- **Supersedes**: pre-existing `frontend/` + `backend/platform/services/*` split

## Context

`deep-research-report (1).md` surveyed monorepo evidence from Google, Meta,
Angular, Kubernetes, Azure SDK JS, Nx, and Rushstack. Three candidate
structures: small-team (asset-type), medium-org (domain-first), large-org
(domain + shared + platform + infra).

## Decision

Hybrid: **small-team variant with Omnix integration baked into `platform/`**.

```
apps/                  # deployable applications (web; future: officer split)
packages/              # reusable libs (contracts, scoring, ts-types, frontend, backend)
services/              # backend microservices (core-api, ats-engine, ai-rewriter, …)
infra/                 # IaC (docker, environments)
platform/              # engineering platform (ci, scripts, build, omnix)
docs/                  # ADRs, architecture, pitch, benchmarks, legacy
tests/                 # cross-domain e2e only
.obsidian-ai-memory/   # long-term engineering memory (Omnix vault)
.omnix/                # Omnix runtime cache (gitignored where appropriate)
.claude/               # project Claude config (per CareerOS .claude image)
.cursor/               # project Cursor rules (existing)
```

Asset-type grouping over domain-first because we have one product domain
(placement readiness) and a small team. If a second domain emerges,
re-evaluate the medium-org variant.

## Why this variant

- Matches the strongest open-source monorepos at our scale: Angular, Azure
  SDK JS, Nx, Rushstack (research §"Open-source monorepos that actually work
  at scale").
- Polyglot-ready: Python services in `services/`, TS app in `apps/web`,
  shared cross-language contracts in `packages/contracts/`.
- Platform layer makes engineering tooling first-class instead of buried in
  the first app that needed it.
- Omnix integration is explicit (`platform/omnix/`) rather than scattered.

## Build orchestration

- **JS side**: pnpm workspaces (locked in via `pnpm-workspace.yaml`). Nx
  orchestration deferred — not enough JS surface area yet.
- **Python side**: each `services/*` self-contained with its own
  `requirements.txt`. Shared Python code (when it lands) goes in
  `packages/scoring/`, `packages/backend/`.
- **Cross-cutting**: `docker-compose.yml` at root composes services.

Nx adoption is deferred until we have >1 JS app or >3 shared TS packages.
Bazel deferred indefinitely — research §"Build systems": "Reserve Bazel for
the point at which native-tool composition is no longer good enough."

## Versioning

Live-at-head internally (research §"Dependency and release strategy").
Independent versioning at the deploy boundary if/when services hit production.
No lockstep coupling between unrelated services.

## Consequences

- Adding a new service: drop it in `services/<name>/`, give it a Dockerfile,
  wire `docker-compose.yml`, optionally consume `packages/contracts/`.
- Adding a shared lib: `packages/<name>/`, document in
  `packages/<name>/README.md`, link from `packages/README.md`.
- Adding cross-domain test: `tests/<scenario>.test.ts`.

## References

- `deep-research-report (1).md` §"Recommended reference architecture",
  §"Small-team variant"
- `C:\Users\ADMIN\.claude\plans\brutal-upgrade-direction-make-humble-parnas.md`
