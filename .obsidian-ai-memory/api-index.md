---
tags: [hub, api, contracts, moc, fastapi]
type: moc
created: 2026-05-21
updated: 2026-05-21
links: [_INDEX, architecture-index, scoring-knowledge, 06-WORKFLOWS/README]
---

# 🔌 API Index — MOC

> Map of Content for HTTP contracts: core-api routes, DTOs, and cross-service clients.  
> Implementation: `services/core-api/app/api/controllers/` → `api/router.py` (legacy routes removed from `main.py`).

← [[_INDEX]] | [[architecture-index]] | [[scoring-knowledge]] | [[06-WORKFLOWS/README]] →

---

## Health

| Method | Path | Auth | Notes |
|--------|------|------|-------|
| GET | `/health` | — | On `main.py` only (not in router) |

---

## Auth — `/auth/*`

| Method | Path | Body / response | Layer |
|--------|------|-----------------|-------|
| POST | `/auth/register` | `RegisterRequest` → `AuthResponse` | [[05-ARCHITECTURE/layered-modules#Phase 2]] |
| POST | `/auth/login` | `LoginRequest` → `AuthResponse` | `auth_controller` |

**DTOs:** `modules/auth/dto/auth_dto.py` · re-export `schemas/contracts.py`

---

## Profile — `/profile`

| Method | Path | Notes |
|--------|------|-------|
| GET | `/profile` | Defaults when row missing — [[01-SESSIONS/2026-05-21/session-1800-cursor]] |
| PUT | `/profile` | `ProfileUpsert` → upsert handler |

**DTOs:** `modules/profile/dto/profile_dto.py`

---

## Resume — `/resumes/*`

| Method | Path | Notes |
|--------|------|-------|
| POST | `/resumes/generate` | AI content via `clients.generate_resume_content` |
| GET | `/resumes` | List for user |
| POST | `/resumes/upload` | Multipart → `resume-parser` |
| GET | `/resumes/{id}` | Detail |
| GET | `/resumes/{id}/sections` | Parsed sections JSON |
| DELETE | `/resumes/{id}` | Owner-scoped |

**Phase:** [[05-ARCHITECTURE/layered-modules#Phase 4]] · Session: [[01-SESSIONS/2026-05-21/session-phases-4-7-cursor]]

---

## Export — `/resumes/export/*`

| Method | Path | Notes |
|--------|------|-------|
| POST | `/resumes/export` | Queue Celery `generate_resume_export` |
| GET | `/resumes/export/{job_id}` | Status + `has_file` |
| GET | `/resumes/export/{job_id}/download` | PDF `FileResponse` or redirect |

**Worker:** `workers/tasks.py` · WeasyPrint — Week 3 hardening in [[MASTER_PLAN#Week 3]]

---

## ATS — `/ats/*`

| Method | Path | Notes |
|--------|------|-------|
| POST | `/ats/scan` | Proxies `ats-engine` `/scan`; persists `ats_scans` |
| GET | `/ats/scans` | History for user |

**Week 2 note:** Narrow `ats-engine` to parse-safety only; full score moves to [[scoring-knowledge]] via match-engine + `packages/scoring/`. See [[02-PROJECTS/active-goals]].

---

## Dashboard — `/dashboard`

| Method | Path | Response |
|--------|------|----------|
| GET | `/dashboard` | `best_ats_score`, `total_resumes`, `scans_performed`, `profile_completeness` |

Officer/student metrics — Week 4 cohort UI in [[MASTER_PLAN#Week 4]].

---

## JD — `/jd/*` (Week 2 — planned)

| Method | Path | Status |
|--------|------|--------|
| POST | `/jd/parse` | ⏳ JD text → `job_descriptions` |
| GET | `/jd/{id}` | ⏳ `skills_json`, `eligibility_json` |

Feeds [[scoring-knowledge#JD_Match sub-formula]].

---

## Scorecards — `/scorecards/*` (Week 2 — planned)

| Method | Path | Status |
|--------|------|--------|
| POST | `/scorecards/score` | ⏳ Resume + JD → 6-component score |
| GET | `/scorecards/{id}` | ⏳ Breakdown for UI bars |

**Formula:** [[scoring-knowledge]] only — never inline in controllers ([[04-DECISIONS/decisions]]).

---

## Rewriter contract (Week 3 — planned)

Not a single core-api path yet; pattern:

| Service | Path | Contract |
|---------|------|----------|
| `ai-rewriter` | POST `/generate/resume` | `ResumePrompt` → `{ content }` |
| core-api (future) | POST `/recommendations/rewrite` | Proof-linked JSON schema |

**Rules:** `evidence_ids[]` required · `unsupported_claims[]` never in `section_rewrites[]` — [[02-PROJECTS/project-context#Important constraints]]

---

## Service clients (`services/core-api/app/services/clients.py`)

| Client function | Target service | Port |
|-----------------|----------------|------|
| `parse_resume_file` | `resume-parser` | 8004 |
| `generate_resume_content` | `ai-rewriter` | 8003 |
| `run_ats_scan` | `ats-engine` | 8001 |
| (Week 2) match/score | `match-engine` | 8005 |

**Rule:** httpx only — never `requests`. Env URLs in `config.py` / `.env.example`.

---

## Frontend client

All browser HTTP via `apps/web/lib/api.ts` — no inline `fetch` in components ([[05-ARCHITECTURE/layered-modules#Phase 6]]).

Module wrappers: `apps/web/modules/auth/services/`, `apps/web/modules/resume/services/`.

---

## Adding endpoints

→ Procedure: [[06-WORKFLOWS/README#Adding a new FastAPI endpoint]]

---

*Related: [[_INDEX]] · [[architecture-index]] · [[scoring-knowledge]] · [[intel-index]] · [[06-WORKFLOWS/README]] · [[05-ARCHITECTURE/layered-modules]] · [[04-DECISIONS/decisions]]*
