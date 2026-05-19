# Code style — CareerOS Campus AI

Applies to all code edits in this repo. This is a polyglot monorepo:
Next.js 14 (apps/web) + FastAPI (services/) + shared Python (packages/scoring/).

## Universal

- No comments explaining *what* — well-named identifiers do that. Comments only for *why*:
  hidden constraint, subtle invariant, known bug workaround, non-obvious side effect.
- No task/PR references in code comments — they belong in the commit message.
- No backwards-compat hacks: no `_unused` renames, no `// removed` markers, no re-export shims.
  If something is unused, delete it.
- Three similar lines is better than a premature abstraction.
- No features, refactors, or abstractions beyond what the task requires.
- No error handling for scenarios that cannot happen. Trust internal code and framework guarantees.
  Validate only at system boundaries (user input, external APIs, file uploads).

## Python — `services/`, `packages/scoring/`, `packages/backend/`

- **SQLAlchemy 2.0 mapped-column style.** `Mapped[T]` / `mapped_column(...)`. No `Column()`.
- **Pydantic v2.** `model_dump()` not `.dict()`. `model_validate()` not `.parse_obj()`.
- **FastAPI route handlers stay slim.** One job: validate, delegate to service layer, return.
- **Type-hint all public functions.** `from __future__ import annotations` for forward refs.
- **httpx for all HTTP**, never `requests`. All cross-service calls via `services/core-api/app/services/clients.py`.
- **Import order:** stdlib → third-party → first-party, blank-line separated.
- **Never commit `__pycache__/` or `*.pyc`.** Covered by `.gitignore`.
- **Config via `os.getenv()`.** Fail fast on missing required config at startup.
- **Celery tasks:** always close the DB session in `finally`.
- **Score formula:** import from `packages/scoring/`. Never duplicate or inline the formula.

## TypeScript — `apps/web/`, `packages/ts-types/`

- **`strict: true`.** No `any`. Truly unknown types → `unknown`, then narrow explicitly.
- **React function components only.** No class components.
- **`"use client"` only when required** (hooks, browser APIs, event handlers). Default: server component.
- **All HTTP via `apps/web/lib/api.ts`.** Never `fetch()` inline in components.
- **State:** `useState` + `useMemo` + `useCareerOSWorkspace`. No global state library without an ADR.
- **No `useEffect` for derived state** — compute in render or `useMemo`.
- **UI primitives first:** `CardSection`, `FormField`, `MetricTile` from `apps/web/components/ui/primitives.tsx`.
- **Styling:** CSS variables in `apps/web/app/globals.css`. No Tailwind, no CSS-in-JS without an ADR.
- **Inline `style={{...}}`** tolerated for one-off tweaks. New reusable components use CSS classes.
- **Import order:** external packages → workspace packages → relative. No barrel re-exports without reason.

## Accessibility (TypeScript components)

- Buttons: `type="button"` or `type="submit"`. No typeless buttons.
- Form fields: `FormField` wrapper with a real `<label>`.
- No `tabIndex="-1"` on interactive controls.
- No `dangerouslySetInnerHTML` without a sanitiser.

## File layout

| Code | Test location |
|---|---|
| `services/<svc>/app/` | `services/<svc>/tests/` |
| `apps/web/` | `apps/web/__tests__/` |
| Cross-service flows | `tests/` (root) only |

- Per-service docs: `services/<svc>/README.md`
- Per-package docs: `packages/<pkg>/README.md`
- Top-level project docs: `docs/`
