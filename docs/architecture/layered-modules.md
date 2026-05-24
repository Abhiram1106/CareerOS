# Layered modular architecture — CareerOS

> Governing standard for backend (`services/core-api`) and frontend (`apps/web`).
> Tooling dirs (`.cursor`, `.claude`, CI) are unchanged.

## Dependency flow (strict)

**Write:** `Frontend → Controller → Handler → Repo → Entity/DB`  
**Read:** `Frontend ← Controller ← QueryService ← View ← Entity/DB`

| Layer | May call | Must not |
|-------|----------|----------|
| Controller | Handler, QueryService, DTO validation | Repo, View, SQL |
| Handler | Repo, other handlers, `clients.py` | View, HTTP details |
| QueryService | View, mappers | Repo (writes), Handler |
| Repo | ORM entities / session | Business rules, joins |
| View | ORM session (read queries) | Writes |
| Entity | — | Business logic |

## Current status

| Phase | State | What |
|-------|--------|------|
| **1 — Scaffold** | Done | Full folder tree + this doc |
| **2 — Auth domain** | Done | `/auth/register`, `/auth/login` via controller → handlers → repos |
| **3 — Profile** | Done | `GET/PUT /profile` via controller → query service / handler → view / repo |
| **4 — Resume + export** | Next | Largest surface |
| **5 — ATS + dashboard** | Pending | Read-heavy |
| **6 — Frontend modules** | After auth API stable | `apps/web/modules/*`, consolidate `lib/api.ts` |
| **7 — Satellite services** | Later | ats-engine, resume-parser, ai-rewriter |

Legacy code remains in `app/main.py` and `app/models/entities.py` until each domain is migrated. **Do not delete legacy paths until the domain’s routes are wired through the new stack.**

---

## Backend target tree (`services/core-api/app/`)

```text
app/
  main.py                          # bootstrap + include routers (slim target)
  create_app.py                    # FastAPI factory (target)
  config.py
  database.py
  db_bootstrap.py
  dependencies.py

  api/
    router.py                      # mounts all domain routers
    controllers/
      health_controller.py
      auth_controller.py
      profile_controller.py
      resume_controller.py
      export_controller.py
      ats_controller.py
      dashboard_controller.py

  modules/
    auth/
      mutation/
      query/
      dto/
      mapper/
      types/
    profile/
      mutation/
      query/
      dto/
      mapper/
      types/
    resume/
      mutation/
      query/
      dto/
      mapper/
      types/
    export/
      mutation/
      query/
      dto/
      mapper/
      types/
    ats/
      mutation/
      query/
      dto/
      mapper/
      types/
    dashboard/
      query/
      dto/
      mapper/
      types/

  adapter/
    db/
      entities/                    # split from models/entities.py (Phase 2+)
      persistence/
        auth/
        profile/
        resume/
        export/
        ats/
        dashboard/

  models/                          # LEGACY — migrate → adapter/db/entities/
    entities.py
  schemas/                         # LEGACY — migrate → modules/*/dto/
    contracts.py
  services/                        # LEGACY infra — keep clients, pdf_export, auth crypto
    auth.py
    clients.py
    pdf_export.py
  workers/
```

### Route → domain map (migration checklist)

| Route | Domain | Handler (write) | Query (read) |
|-------|--------|-----------------|--------------|
| `POST /auth/register` | auth | `register.handler` | — |
| `POST /auth/login` | auth | `login.handler` | — |
| `GET/PUT /profile` | profile | `update-profile.handler` | `profile-query.service` |
| `POST /resumes/generate` | resume | `generate-resume.handler` | — |
| `POST /resumes/upload` | resume | `upload-resume.handler` | — |
| `GET/DELETE /resumes/*` | resume | `delete-resume.handler` | `resume-query.service` |
| `POST /resumes/export` | export | `queue-export.handler` | — |
| `GET /resumes/export/*` | export | — | `export-query.service` |
| `POST /ats/scan` | ats | `run-ats-scan.handler` | — |
| `GET /ats/scans` | ats | — | `ats-query.service` |
| `GET /dashboard` | dashboard | — | `dashboard-query.service` |

---

## Frontend target tree (`apps/web/`)

> Stack today is **Next.js 14** (not a separate RN app). Same module mental model applies.

```text
apps/web/
  app/                             # Next.js routes (thin — compose modules only)
  lib/
    api.ts                         # ALL HTTP (canonical)
    auth.ts
  hooks/
    useCareerOSWorkspace.ts        # LEGACY — split per module later
  components/                      # LEGACY shared UI — promote to shared/ over time
    ui/
    layout/
    marketing/
    workspace/
    panes/

  modules/                         # feature-first, flat files only
    auth/
    assistant/
    intel/
    resume/
    scorecard/

  shared/                          # NEW — aliases / docs for cross-module UI
    README.md
```

### Frontend migration checklist

- [ ] `login` / `register` pages → `modules/auth/authService.ts`
- [ ] `workspace/page.tsx` upload `fetch` → `lib/api.ts`
- [ ] Types from `components/panes/types.ts` → `modules/*/types.ts`
- [ ] Single auth token key (`cos_auth` via `lib/auth.ts`)

---

## Naming conventions

- Python: `snake_case` files; handlers `verb_noun.handler.py`; query `noun_query.service.py`
- TS: `camelCase` functions; `PascalCase` types; services `authApi.ts` etc.

---

## Next step (do this first in Agent mode)

**Phase 2 — Migrate `auth` domain end-to-end** (smallest, proves the pattern):

1. `RegisterHandler` + `LoginHandler` + `SessionRepo` + `UserRepo`
2. `auth_controller.py` with two routes
3. Mount router in `api/router.py`; include from slim `main.py`
4. Remove auth routes from `main.py` only after parity test
5. AST-parse all touched Python files

Then **profile**, then **resume** (largest).

---

_Last updated: 2026-05-21_
