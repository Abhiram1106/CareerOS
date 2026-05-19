# React / Next.js rules — apps/web

Applies to `apps/web/**/*.{ts,tsx}`.

## App router

- App router only (`apps/web/app/`). No pages router.
- Default: server component. Mark `"use client"` only when the file needs hooks,
  browser APIs, or event handlers — not as a default.
- Route groups enforce role separation:
  - `apps/web/app/(student)/` — student surface: resume upload, ATS scan, score view (Week 1–3)
  - `apps/web/app/(officer)/` — officer surface: dashboard, batches, JDs, review queue (Week 4)
  - `apps/web/app/lab/` — Intel benchmark panel (Week 5)
- Route-specific components stay in the route folder. Promote to `apps/web/components/`
  only when used in 2+ routes.

## State — current shape

- `useCareerOSWorkspace` (`apps/web/hooks/useCareerOSWorkspace.ts`) is the canonical
  cross-pane state hook for the student surface.
- When the officer surface lands (Week 4): split into `useStudentWorkspace` and
  `useOfficerWorkspace`. Do not add officer state to the existing student hook.
- `localStorage` for auth token only. Every other piece of data is server-derived.
- No Redux, Zustand, Jotai, or other global state library without an ADR.

## What NOT to do

- No `useEffect` for derived state — compute in render or `useMemo`.
- No data fetching inside `useEffect` when data is route-stable — use server components.
- No `fetch()` inline in components — use `apps/web/lib/api.ts`.
- No `...rest` spreads on props unless the component wraps a real DOM element.
- No `dangerouslySetInnerHTML` without a sanitiser.
- No `tabIndex="-1"` on interactive controls.

## API layer

- All HTTP calls via `apps/web/lib/api.ts`.
- Auth token attached centrally in `api.ts`. Components receive and pass `token` as an arg.
- New backend endpoints get a typed wrapper function added to `api.ts` before use.

## UI conventions

- Use `CardSection`, `FormField`, `MetricTile` from `apps/web/components/ui/primitives.tsx`
  before writing new layout components.
- Pane-level components: `apps/web/components/panes/<PaneName>Pane.tsx`.
- Section cards (sub-pane cards): `apps/web/components/panes/sections/<Name>Card.tsx`.

## Styling

- CSS variables in `apps/web/app/globals.css` for the dark theme. Extend, never replace.
- Inline `style={{...}}` tolerated for one-off spacing on existing components.
  New reusable layout → CSS class in `globals.css`.
- No Tailwind, no CSS-in-JS, no styled-components until an explicit ADR approves it.

## Types

- All pane-level state types in `apps/web/components/panes/types.ts`.
- Domain types (Resume JSON, JD JSON, Scorecard, Rewrite) consumed from `packages/ts-types/`
  once `packages/contracts/schemas/` ships.
- `strict: true` enforced via `apps/web/tsconfig.json`. Verify with `tsc --noEmit`.

## Accessibility baseline

- Every `<button>` has a `type` attribute.
- Every form field rendered via `FormField` has a real `<label>`.
- All interactive controls are keyboard-reachable.
