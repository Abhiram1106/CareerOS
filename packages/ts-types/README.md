# packages/ts-types/

TypeScript types generated from `packages/contracts/schemas/*.json`.

Consumed by `apps/web` via the pnpm workspace. Do **not** hand-edit files in
this package — regenerate from contracts instead. Codegen wiring lands in the
follow-up commit once the first schema (`scorecard.schema.json`) ships.

```bash
pnpm --filter ts-types run codegen
```
