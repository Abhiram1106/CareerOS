---
tags: [project, snapshot, verification, ux]
type: project
updated: 2026-05-29
links: [_INDEX, architecture-index, session-index]
---

# Current State

Last scanned: 2026-05-29.

Latest update: student UX architecture moved from tab-centric workspace to route-per-workflow product shell.

## Stack

- Web: Next.js 14 + TypeScript strict
- API: FastAPI 0.115
- Data: PostgreSQL + Redis
- Scoring: packages/scoring as single source of truth

## Product surfaces

| Surface | Status |
|---|---|
| `/dashboard` command center | Live |
| `/resume` upload/parse/generate/export | Live |
| `/match` JD scan + readiness breakdown | Live |
| `/rewrite` proof-linked rewrite | Live |
| `/jobs` search + score-me CTA | Live |
| `/assistant` persistent chat + score context | Live |
| `/settings` profile completeness surface | Live |
| `/workspace*` legacy tab routes | Redirect only |
| `/lab/intel` | Live, demoted to secondary nav |

## Frontend architecture changes

- New authenticated shell: left rail (desktop) + bottom nav (mobile)
- Topbar now shows profile completeness + user controls
- Global toast system added and wired to async actions
- Workspace persistence added via localStorage:
  - `resume_id`
  - `jd_text`
  - latest score snapshot
  - active tab
- Assistant history persisted in localStorage

## Verification (2026-05-29)

| Check | Result |
|---|---|
| `npx tsc --noEmit` (apps/web) | pass |
| Python AST parse (`services/**/*.py`) | pass |
| Alembic upgrade | skipped (frontend-only session) |

## Open risks

1. `/match/[scorecard_id]` permalink still needs backend read endpoint for true shareability.
2. Builder flow has been de-emphasized; if retained, it should be reintroduced as a first-class route.
3. Additional responsive QA is still needed at 360px and 768px breakpoints.
