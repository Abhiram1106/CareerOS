# React / Next.js rules — apps/web

Applies to `apps/web/**/*.{ts,tsx}`.

## Next.js 14 app router

- App router only (`apps/web/app/`). No pages router.
- Default to server components. Mark `"use client"` only when the file
  actually needs hooks, browser APIs, or event handlers.
- Route groups for role separation: future officer surface lives under
  `apps/web/app/(officer)/`, student under `apps/web/app/(student)/`.
- Co-locate route-specific components in the route folder; promote to
  `apps/web/components/` only when used in 2+ routes.

## State

- Single workspace hook pattern (`useCareerOSWorkspace`) is the canonical
  shape for cross-pane state. Split by role (`useStudentWorkspace`,
  `useOfficerWorkspace`) when officer pane lands.
- No Redux / Zustand / Jotai unless a concrete reason emerges.
- `localStorage` only for auth token. Everything else server-derived.

## API

- All HTTP via `apps/web/lib/api.ts` typed client. Never `fetch()` inline
  in components.
- Auth header attached centrally in `api.ts`. Components pass `token`.

## Styling

- CSS variables in `apps/web/app/globals.css` (dark theme tokens).
  Extend, don't replace.
- Existing patterns use inline `style={{ marginTop: 12 }}` for one-offs;
  new components should prefer CSS classes when the styling is reusable.
- No CSS-in-JS, no styled-components, no Tailwind until a deliberate
  decision lands as an ADR.

## Components

- Use the primitives in `apps/web/components/ui/primitives.tsx`
  (`CardSection`, `FormField`, `MetricTile`).
- Pane components live in `apps/web/components/panes/`, section cards in
  `apps/web/components/panes/sections/`.
- Props are explicit. No `...rest` spreads unless wrapping a real DOM
  element.

## Accessibility

- Buttons must have a `type` attribute (`button` for non-submit, `submit`
  in forms).
- Form fields wrap in `FormField` with a real `label`.
- Keyboard reachable; don't `tabindex="-1"` interactive controls.

## Anti-patterns

- No `dangerouslySetInnerHTML` without a sanitizer.
- No `useEffect` for derived state — compute in render or `useMemo`.
- No fetching inside `useEffect` if the data is route-stable — use server
  components or route loaders.
