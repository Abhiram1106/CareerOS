# Frontend modules (feature-first)

Screens stay in `app/` (Next.js App Router). Modules own:

- `services/` — calls `lib/api.ts` only (no inline `fetch` in screens)
- `types/` / `dto/` — module contracts
- `hooks/` / `store/` — module state (extracted from `usePlacementWorkspace` as features grow)

Shared UI: see `../shared/README.md` and existing `../components/ui/`.
