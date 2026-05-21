# Layered modular architecture — CareerOS

> **Load this for any refactor, new endpoint, or “where does this code go?” question.**
> Repo mirror (same content, kept in sync): `docs/architecture/layered-modules.md`
> Entry pointer: `services/core-api/LAYERED_ARCHITECTURE.md`

_Last updated: 2026-05-21 — Phases 1–3 done (scaffold, auth, profile)._

---

## Dependency flow (strict)

**Write:** `Frontend → Controller → Handler → Repo → Entity/DB`  
**Read:** `Frontend ← Controller ← QueryService ← View ← Entity/DB`

| Layer | May call | Must not |
|-------|----------|----------|
| Controller | Handler, QueryService, DTOs | Repo, View, SQL |
| Handler | Repo, `clients.py`, other handlers | View, HTTP |
| QueryService | View, mappers | Repo (writes), Handler |
| Repo | ORM / session (writes) | Business rules, heavy joins |
| View | ORM / session (reads) | Writes |
| Entity | — | Business logic |

**Infra (not domain logic):** `app/services/auth.py` (JWT/hash/verify/token decode), `clients.py`, `pdf_export.py`, `workers/`.

---

## Migration status (update when a phase lands)

| Phase | Status | Scope |
|-------|--------|--------|
| 1 Scaffold | **Done** | Folders under `app/modules/`, `app/api/`, `app/adapter/db/`; `apps/web/modules/`, `shared/` |
| 2 Auth | **Done** | `POST /auth/register`, `POST /auth/login` |
| 3 Profile | **Done** | `GET/PUT /profile` |
| 4 Resume + export | **Next** | Largest |
| 5 ATS + dashboard | Pending | Read-heavy |
| 6 Frontend modules | Pending | `lib/api.ts` only; no inline `fetch` |
| 7 Satellite services | Pending | ats-engine, resume-parser, ai-rewriter |

**Rule:** Do not remove legacy routes from `main.py` until the domain is wired through `api/router.py`.

---

## What is migrated today

**Auth**

```
POST /auth/register | POST /auth/login
  → api/controllers/auth_controller.py
  → modules/auth/mutation/
  → adapter/db/persistence/auth/
```

**Profile**

```
GET /profile | PUT /profile
  → api/controllers/profile_controller.py
  → modules/profile/query/profile_query_service.py + profile_view.py  (read)
  → modules/profile/mutation/upsert_profile_handler.py + profile_repo.py  (write)
```

DTOs: `modules/auth/dto/auth_dto.py`, `modules/profile/dto/profile_dto.py` (re-exported from `schemas/contracts.py`).

---

## Backend tree on disk (`services/core-api/app/`)

```text
main.py                    # LEGACY routes + app.include_router(api_router)
api/
  router.py                # mounts domain routers
  controllers/
    auth_controller.py     # DONE
    profile_controller.py  # DONE
    (resume, export, ats, dashboard — pending)

modules/
  auth/     mutation/ query/ dto/ mapper/ types/   # DONE
  profile/  mutation/ query/ dto/ mapper/ types/   # DONE
  resume/   ...
  export/   ...
  ats/      ...
  dashboard/ query/ ...  (no mutation/)

adapter/db/
  entities/                # empty — entities still in models/entities.py
  persistence/
    auth/     user_repo.py, session_repo.py
    profile/  profile_repo.py, profile_view.py
    resume/ export/ ats/ dashboard/  (scaffold only)

models/entities.py         # LEGACY — all ORM models
schemas/contracts.py       # LEGACY — non-auth DTOs; auth re-exports auth module
services/                  # auth.py (crypto), clients.py, pdf_export.py
workers/
```

---

## Frontend tree on disk (`apps/web/`)

```text
app/                       # Next.js routes (unchanged)
lib/api.ts                 # canonical HTTP
components/                # LEGACY shared UI (still in use)
modules/                   # SCAFFOLD — feature folders empty except README
  auth/ profile/ resume/ ats/ dashboard/ officer/
  each: services/ types/ dto/ hooks/ store/
shared/                    # SCAFFOLD — target for cross-module UI
```

**Note:** Product is Next.js 14, not a separate React Native app. Same module mental model applies.

---

## Adding an endpoint (migrated domain)

1. DTO → `modules/<domain>/dto/`
2. Write → `modules/<domain>/mutation/<verb>_handler.py` + `adapter/db/persistence/<domain>/*.repo.py`
3. Read → `modules/<domain>/query/<domain>_query.service.py` + `*.view.py` (if joins needed)
4. HTTP → `api/controllers/<domain>_controller.py`
5. Register router in `api/router.py`
6. Remove duplicate route from `main.py`
7. `apps/web/lib/api.ts` wrapper + verify AST + tsc

**Unmigrated domain:** still use `main.py` + `schemas/contracts.py` until that domain’s phase completes (see workflow in `06-WORKFLOWS/README.md`).

---

## For the next agent

1. Read this file + `02-PROJECTS/current-state.md`
2. Continue **Phase 4 — resume + export** (see latest session in `01-SESSIONS/2026-05-21/`)
3. Follow `.cursor/rules/backend.mdc` and `.cursor/context/backend-context.md`
4. Do not duplicate PlacementReadinessScore outside `packages/scoring/`
