# Code style — CareerOS Campus AI

Applies to all code edits in this repo.

## General

- Trust internal code and framework guarantees. Validate only at system
  boundaries (user input, external APIs).
- Don't add error handling, fallbacks, or validation for scenarios that
  can't happen.
- Don't add features, refactor, or introduce abstractions beyond what the
  task requires. Three similar lines beats a premature abstraction.
- Default to writing no comments. Add one only when *why* is non-obvious
  (hidden constraint, subtle invariant, workaround for a specific bug).
  Never explain *what* — names already do that.
- Don't reference the current task, fix, or callers in comments ("used by
  X", "added for the Y flow"). That belongs in the PR description.
- No backwards-compat hacks (renaming unused `_vars`, re-export shims,
  `// removed` markers). If unused, delete it.

## Python (services/, packages/scoring/)

- Type-hint public functions. Use `from __future__ import annotations` if
  forward refs proliferate.
- SQLAlchemy 2.0 mapped-column style (`Mapped[T]` / `mapped_column(...)`).
- FastAPI routers stay slim — business logic in `services/<svc>/app/services/`,
  not in route handlers.
- Pydantic v2 (BaseModel + Field). Email validation via `EmailStr`.
- `__pycache__/` and `*.pyc` are gitignored; never check in.

## TypeScript (apps/web/, packages/ts-types/)

- `strict: true`. No `any`. If a type is unknown, use `unknown` and narrow.
- React function components only.
- State management: `useState` + `useMemo`. No global state library until
  there's a concrete need.
- Inline styles are tolerated where they already exist (`style={{...}}`);
  new components should prefer CSS classes in `globals.css`.
- Use the typed `lib/api.ts` client. Don't `fetch()` directly from
  components.

## Imports

- Python: stdlib → third-party → first-party, separated by blank lines.
- TypeScript: external → workspace packages → relative.
- No barrel files (`index.ts` re-exports) unless they remove real ceremony.

## File layout

- Tests next to code (`services/<svc>/tests/`, `apps/web/__tests__/`).
- Cross-domain e2e in `tests/` only.
- Per-service docs in the service's `README.md`, top-level docs in
  `docs/`.
