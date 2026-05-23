---
tags: [session, frontend, demo-removal, workspace]
tool: cursor
date: 2026-05-21
---

# Session digest — Demo mode removed, production workspace

## Goal

Remove `NEXT_PUBLIC_DEMO` and synthetic flows; wire workspace to real core-api only with maintainable structure.

## Done

- Removed `DEMO_USERS`, demo login bypass, app demo banner, workspace fake delays/sample data.
- **`apps/web/hooks/usePlacementWorkspace.ts`** — upload, score, generate, export; `cos_auth` via `getStoredAuth()`.
- **`apps/web/lib/placement.ts`** — score component meta, ATS flag normalization, bucket helpers, templates.
- **`apps/web/components/workspace/`** — `ResumeDropzone`, `ScoreBreakdown`.
- **`apps/web/app/(app)/workspace/page.tsx`** — refactored to hook; real `api.scoreResume` with raw bar scores.
- **`useCareerOSWorkspace.ts`** — migrated token storage from `careeros_token` to `storeAuth` / `clearAuth`.
- **`apps/web/.env.example`** — `NEXT_PUBLIC_CORE_API_URL` only; `.env.local` demo flag removed.
- **`modules/scorecard/services/scorecardService.ts`** — thin wrapper over `api.scoreResume`.

## Verify

- `tsc --noEmit` (apps/web): clean
- No `NEXT_PUBLIC_DEMO` / `DEMO_USERS` references under `apps/web`

## Open

- E2E manual: stack up (`docker compose up`), login, upload → score with match-engine healthy.
- `useCareerOSWorkspace` still uses legacy `/ats/scan` for pane UI if re-enabled.

## Key paths

| Piece | Path |
|-------|------|
| Workspace hook | `apps/web/hooks/usePlacementWorkspace.ts` |
| Workspace UI | `apps/web/app/(app)/workspace/page.tsx` |
| Auth storage | `apps/web/lib/auth.ts` (`cos_auth`) |
