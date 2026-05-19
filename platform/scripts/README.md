# platform/scripts/

Repo-level dev tooling. Anything an engineer should be able to run from the
repo root.

Reserved targets:
- `bootstrap.{sh,ps1}` — install pinned tools + verify Node/Python/pnpm
- `codegen.{sh,ps1}` — regenerate `packages/ts-types/` from `packages/contracts/schemas/`
- `seed-dev.{sh,ps1}` — populate dev Postgres with sample colleges/batches/JDs

Empty for now. Lands in Week 1 once the first schema exists.
