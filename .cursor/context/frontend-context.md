# Frontend Context — CareerOS Student AI
# @include this file when working in `apps/web/`

## App structure

```text
apps/web/
  app/                # Next.js App Router screens
  components/         # shared UI and page-level components
  hooks/              # cross-feature hooks
  lib/                # typed API client + auth helpers
  modules/            # feature modules (flat, only real code)
```

## Module rules (flat feature slices)

- Keep only files that execute today.
- Prefer:
  - `<feature>Service.ts`
  - `use<Feature>.ts` (if needed)
  - `types.ts` (if needed)
- No placeholder `dto/`, `hooks/`, `store/`, or `types/` directories unless they contain active code.

## Data and networking rules

- All HTTP calls go through `apps/web/lib/api.ts`.
- Components do not call `fetch` directly.
- Auth token handling stays centralized in `lib/auth.ts`.

## Styling rules

- Use global CSS variables from `app/globals.css`.
- No Tailwind or CSS-in-JS.

## Product scope

- Student workflows only: resume upload, ATS analysis, scorecard, rewrite guidance, export, jobs, assistant.
