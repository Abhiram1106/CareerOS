# packages/

Reusable libraries shared across `apps/` and `services/`. Nothing in here is
deployable on its own — if it runs, it belongs in `apps/` or `services/`.

| Folder | Purpose | Status |
|---|---|---|
| `contracts/openapi/` | OpenAPI specs emitted from `services/core-api`. Source of truth for HTTP contracts. | Skeleton |
| `contracts/schemas/` | JSON Schema files for cross-language data shapes: `Resume`, `JD`, `Scorecard`, `Rewrite`. Consumed by Python services and `ts-types/` codegen. | Skeleton |
| `scoring/` | Python package implementing the **PlacementReadinessScore** formula (research §"Hybrid JD match and scoring model"). Imported by `services/core-api` and `services/intel-bench`. | Skeleton |
| `ts-types/` | TypeScript types generated from `contracts/schemas/`. Consumed by `apps/web`. | Skeleton |
| `frontend/` | Future home for shared React components and design tokens. | Reserved |
| `backend/` | Future home for shared Python utilities (auth, observability, etc.). | Reserved |

## Versioning

Internal-only. Source dependencies via workspace protocol (`workspace:*` for JS,
relative import for Python). No published versions until a package needs an
external consumer.

## Why this exists

Research §"Recommended reference architecture": shared contracts/schemas go in
`packages/` so multiple deployables can consume them without duplicating
definitions. Cross-language source sharing is anti-pattern; **share contracts
and generate clients** instead.
