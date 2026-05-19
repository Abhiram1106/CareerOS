# Frontend Context — CareerOS Campus AI
# @include this file when working in apps/web/

## App structure

```
apps/web/
  app/
    page.tsx          — Root page: AppView state (overview | workspace)
    layout.tsx        — HTML root, metadata, fonts
    globals.css       — All CSS: variables, components, layout, pane styles
  components/
    layout/
      AppHeader.tsx   — Sticky top bar: brand + AppView nav + status chip
      SiteNav.tsx     — Overview/Workspace toggle buttons
      AppFooter.tsx   — Footer with roadmap note
    marketing/
      HeroPage.tsx    — Product hero: stats, feature pillars, workflow steps
    workspace/
      WorkspaceTabs.tsx — Accessible ARIA tablist: Account | Resume & ATS | Readiness
    panes/
      AccountPane.tsx — Auth + profile
      ResumePane.tsx  — Upload card + section viewer + ATS scan
      JobsPane.tsx    — Readiness snapshot (→ officer JDs manager in Week 4)
      sections/       — Sub-pane cards (AtsScanCard, ResumeBuilderCard, etc.)
      types.ts        — ActivePane, AppView, Scan, Dashboard, ParseResult, etc.
    SectionNav.tsx    — @deprecated; use WorkspaceTabs
    ui/primitives.tsx — CardSection, FormField, MetricTile
  hooks/
    useCareerOSWorkspace.ts — Central state: auth, profile, resume, scan, parse
  lib/
    api.ts            — Typed HTTP client: ALL fetch() calls go here
```

## Navigation model

Single route `/` with `AppView` state:
- `"overview"` → renders `<HeroPage />` inside `<AppHeader />`
- `"workspace"` → renders `<WorkspaceTabs />` (Account | Resume & ATS | Readiness)

The `AppHeader` shows the active view toggle. `SiteNav` drives `setAppView`.
Week 4: officer surface gets its own route group `app/(officer)/`.

## State hook — useCareerOSWorkspace

Central state for the student workspace. Key fields:
- `auth`, `setAuth` — login form state
- `token` — JWT (from localStorage)
- `profile`, `setProfile` — career profile
- `scan`, `history` — ATS scan results
- `parseResult`, `uploading` — resume upload + parse results
- `dashboard` — readiness metrics
- `onUploadResume(file)` — calls `/resumes/upload` → sets `parseResult`

Splitting into `useStudentWorkspace` + `useOfficerWorkspace` when Week 4 lands.

## API layer rules (strict)

- ALL fetch() calls in `apps/web/lib/api.ts`
- `request<T>()` for JSON endpoints; `uploadFile<T>()` for multipart
- Auth header attached centrally — components pass `token` as arg
- New endpoint → add typed wrapper to `api.ts` BEFORE using it in a component

## CSS rules (strict)

- Variables defined in `globals.css` — never replace, only extend
- NO Tailwind, NO CSS-in-JS, NO styled-components
- Inline `style={{}}` only for one-off values that reference CSS variables
- New reusable patterns → CSS class in `globals.css`
- Key variables: `--bg`, `--surface`, `--surface-soft`, `--ink`, `--muted`, `--line`

## Component conventions

- `CardSection` for all pane cards — import from `components/ui/primitives.tsx`
- `FormField` for all form fields with labels
- `MetricTile` for numeric dashboard tiles
- `"use client"` only if the component uses hooks, browser APIs, or event handlers
- Buttons: always `type="button"` (non-submit) or `type="submit"` (in forms)
- Hidden file inputs: must have `id` + matching `<label htmlFor>` or `aria-label`

## TypeScript

- `strict: true` — no `any`
- Pane state types in `components/panes/types.ts`
- Domain types (Resume JSON, JD, Scorecard, Rewrite) from `packages/ts-types/` when ready

## Current week's active components

- **ResumePane**: upload card (working) + section viewer (working) + ATS scan (working)
- **WorkspaceTabs**: hero ↔ workspace navigation (working)
- **Next (Week 2)**: JD paste input + score breakdown bars in ResumePane
