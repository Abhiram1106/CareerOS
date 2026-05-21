---
tags: [architecture, frontend, ux]
type: architecture
updated: 2026-05-21
links: [architecture-index, 05-ARCHITECTURE/layered-modules]
---

# Frontend UX — CareerOS Campus AI

← [[architecture-index]] · [[05-ARCHITECTURE/layered-modules]]

_Last updated: 2026-05-21 (module scaffold note + 2026-05-20 shell)._

## Product surfaces (current)

| Surface | Route | Status | Audience |
|---|---|---|---|
| Overview (hero) | `/` — client view `overview` | **Live** | Visitors, TPO demos |
| Student workspace | `/` — client view `workspace` | **Live** | Students |
| Officer dashboard | `(officer)/` route group | Week 4 | Placement officers |

Navigation is **single-page** (`app/page.tsx`) with two top-level views toggled in React state (`AppView`). No separate `/workspace` URL yet — keeps Week 1–2 demo simple; split routes when officer surface lands.

## Information architecture

```
AppHeader (sticky)
├── Brand: CareerOS Campus AI
├── SiteNav: Overview | Workspace
└── Status pill (workspace hook status)

Overview (HeroPage)
├── Hero: positioning + CTAs
├── Feature pillars (4 cards)
└── Workflow steps (4) + CTA

Workspace (workspace-shell)
├── Workspace header + "Back to overview"
├── WorkspaceTabs (underline tabs)
│   ├── Account — auth + profile
│   ├── Resume & ATS — upload, generate, export, JD scan
│   └── Readiness — dashboard snapshot (officer UI Week 4)
└── Tab panels (existing panes, unchanged API wiring)

AppFooter
```

## Component map

| Path | Role |
|---|---|
| `components/layout/AppHeader.tsx` | Sticky chrome, brand, site nav, status |
| `components/layout/SiteNav.tsx` | Overview ↔ Workspace |
| `components/layout/AppFooter.tsx` | Roadmap + scoring package note |
| `components/marketing/HeroPage.tsx` | Product story, demo loop, exclusions |
| `components/workspace/WorkspaceTabs.tsx` | Accessible tablist for panes |
| `components/panes/*` | Account, Resume, Jobs (readiness) |
| `components/ui/primitives.tsx` | CardSection, FormField, MetricTile |
| `hooks/useCareerOSWorkspace.ts` | Auth, API, pane state |
| `lib/api.ts` | Typed core-api client |

`components/SectionNav.tsx` is deprecated; use `WorkspaceTabs`.

## Types

- `AppView`: `"overview" | "workspace"`
- `ActivePane`: `"account" | "resume" | "jobs"` (jobs pane labeled **Readiness** in UI)

## Styling rules

- **No Tailwind** — CSS variables + classes in `app/globals.css` only.
- Fonts: **DM Sans** (display) + **Manrope** (body) via Google Fonts in `layout.tsx`.
- Palette: navy accent (`--accent`, `--accent-ink`), Intel blue highlight (`--intel`), light enterprise surfaces.
- Buttons: `btn-primary`, `btn-secondary`, `btn-ghost`, `btn-compact`; default `button` = primary actions in cards.

## Hero copy constraints (do not drift)

- **Is**: placement-readiness operating layer for Indian colleges; ATS-safe resumes; JD match; proof-linked rewrite; Intel-measured benchmarks.
- **Is not**: job board, LinkedIn scraper, recruiter platform, billing product.
- **Scoring**: formula only in `packages/scoring/` — never duplicate in UI copy as a second implementation.

## Accessibility

- Site nav: `aria-current="page"` on active link.
- Workspace: `role="tablist"` / `role="tab"` / `role="tabpanel"` with `aria-selected`, `aria-controls`, `aria-describedby`.
- All nav buttons: `type="button"`.
- Focus: `:focus-visible` outline on interactive controls.

## Module folders (scaffold — 2026-05-21)

Target layout under `apps/web/` (Phase 6 — not wired yet):

```text
modules/{auth,profile,resume,ats,dashboard,officer}/
  services/  hooks/  types/  dto/  store/
shared/   # cross-module UI primitives (future)
```

**Rules:** all HTTP via `lib/api.ts`; no inline `fetch` in pages. See [[05-ARCHITECTURE/layered-modules]] for full phase table.

## Verification (2026-05-20)

- `pnpm exec tsc --noEmit` — pass
- `pnpm build` — pass

## Next UX (not in scope this session)

- Route groups `(student)/` and `(officer)/` with dedicated URLs
- Officer cohort heatmap pane (Week 4)
- Dark theme toggle (needs ADR if requested)

*Related: [[architecture-index]] · [[05-ARCHITECTURE/layered-modules]] · [[05-ARCHITECTURE/README]] · [[api-index]] · [[session-index]] · [[01-SESSIONS/2026-05-20/session-1430-cursor]]*
