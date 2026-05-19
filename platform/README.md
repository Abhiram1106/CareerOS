# platform/

Repo-level engineering system. Per research §"Recommended reference
architecture": build/CI/policy logic belongs at the top level, not buried
inside the first app that needed it.

| Folder | Purpose | Status |
|---|---|---|
| `ci/` | Shared GitHub Actions workflows + reusable composite actions. The actual workflows live in `.github/workflows/` (consumed paths); reusable bits source here. | Skeleton |
| `scripts/` | Bootstrap, codegen, dev tooling. `bin/bootstrap` lands here. | Skeleton |
| `build/` | Build presets (tsconfig base, lint config, prettier config) for the JS side. JVM/Python don't need this layer yet. | Skeleton |
| `omnix/` | Omnix Runtime committed configuration (agents, workflows, commands, settings). The runtime cache `.omnix/memory/` stays at repo root and is gitignored. | Active — see `omnix/README.md` |

## Why this exists

Engineering tooling should be visible and ownable, not invisible. A repo-level
`platform/` makes it clear where to add new dev ergonomics, what's shared, and
who owns it (see `CODEOWNERS`).
