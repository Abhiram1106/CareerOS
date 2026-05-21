# Core API — layered architecture

Physical scaffold is under `app/modules/`, `app/api/controllers/`, `app/adapter/db/persistence/`.

**Full tree, route map, and phase plan:** [`docs/architecture/layered-modules.md`](../../docs/architecture/layered-modules.md)

## Migration status (phases 1–7)

| Phase | Domain | Routes | Status |
|-------|--------|--------|--------|
| 1 | Scaffold | — | Done |
| 2 | Auth | `POST /auth/register`, `/auth/login` | Done |
| 3 | Profile | `GET/PUT /profile` | Done |
| 4 | Resume + Export | `/resumes/*`, `/resumes/export/*` | Done |
| 5 | ATS + Dashboard | `POST /ats/scan`, `GET /ats/scans`, `GET /dashboard` | Done |
| 6 | Frontend modules | `apps/web/modules/*` → `lib/api.ts` | Done |
| 7 | Satellites | ats-engine, resume-parser, ai-rewriter | Done |

`app/main.py` is health + startup only. All HTTP routes mount via `app/api/router.py`.

Legacy re-exports: `app/schemas/contracts.py` → domain DTOs.

Entities: `app/models/entities.py`
