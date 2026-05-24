---
tags: [project, goals, week-plan, security, kirito]
type: project
updated: 2026-05-23
links: [MASTER_PLAN, _INDEX, scoring-knowledge, security-architecture]
---

# Active Goals

← [[MASTER_PLAN]] · [[05-ARCHITECTURE/security-architecture]] · [[_INDEX]]

> **Kirito roadmap:** All remaining phases prioritize **CIA** (confidentiality, integrity, availability), cryptography, secure networking, and production-grade auth/API design. Full checklist: [[05-ARCHITECTURE/security-architecture]] · Repo ADR: `docs/adr/0007-security-first-future-phases.md`.

---

## Completed foundation (Weeks 1–3 + pivot)

### Week 1
- [x] Monorepo scaffold, Alembic schema, JWT roles, resume parser, layered core-api

### Week 2
- [x] Match-engine, `packages/scoring`, scorecard API + UI

### Audit hardening
- [x] RBAC (`require_student` / `require_officer`), honest semantic labels, golden-path tests, persistence fixes

### Week 3
- [x] Proof-linked rewriter, recommendations API, diff UI, PDF export

### Student-first pivot (2026-05-23)
- [x] `jobs-feed`, deterministic agent, Jobs/Builder UI, sklearnex benchmark doc, ADR 0006, officer flags default-off

### Week 5 (partial)
- [x] sklearnex measured benchmark, demo script, enterprise README

---

## Phase 4 — Officer dashboard + security hardening (NEXT)

> **Gate:** Officer routes must not ship to production until every **Security (blocking)** item is checked.

### Product
- [x] Officer cohort API `GET /officer/cohort` (live aggregates from scorecards)
- [x] `apps/web/(officer)/` — dashboard, review, batches wired to live APIs
- [x] Batch upload, dept heatmap, skill-gap chart (company-fit columns deferred)
- [x] Readiness PDF report export for TPO (`GET /officer/reports/readiness`)
- [ ] Enable officer surface only after review: `ENABLE_OFFICER_SURFACE=true`

### Security (blocking)
- [x] **IDOR prevention:** resume/agent_run/export scoped to `user_id` (+ tests in `test_security_idor.py`)
- [x] **OpenAPI:** `packages/contracts/openapi/core-api.openapi.json` via `scripts/export_openapi.py`
- [x] **API validation:** Pydantic `extra=forbid` on sensitive DTOs via `StrictModel` + `test_validation_strict.py`
- [x] **Rate limiting:** in-process middleware on auth, upload, `/agent/run`
- [x] **Security headers:** CSP, X-Frame-Options, nosniff, HSTS when HTTPS
- [x] **Audit log:** login, logout, export queue, agent complete, officer cohort view
- [x] **Session hardening:** `POST /auth/logout` revokes `session_tokens`
- [x] **DI cleanup:** handler factories in `handler_dependencies.py` (re-exported from `dependencies.py`)
- [x] **Tests:** IDOR + RBAC + headers (`test_security_idor.py`)
- [x] **Threat model:** expanded `docs/security/threat-model.md` (officer, assistant, strict DTOs, DI)

### Infrastructure
- [x] Prod compose profile: `docker-compose.prod.yml` + `docs/deployment/production.md`
- [x] Internal-only ports for parser/match/rewriter (`docker-compose.prod.yml` clears match-engine/jobs-feed host ports)

---

## Phase 5 — Intel lab + production posture

### Product
- [x] `services/intel-bench` — harness (sklearnex measured; OpenVINO/KMeans skipped on Py3.13)
- [x] `apps/web/lab/intel` — benchmark panel wired to `GET /benchmarks`
- [x] 6-slide pitch deck (`docs/pitch/deck.md`), screenshot guide (`docs/pitch/screenshots/`)

### Security (blocking)
- [x] CI dependency audit (`pip-audit`, `pnpm audit`) — fail on critical
- [x] `AUTO_CREATE_TABLES=false` in prod documentation; Alembic-only schema
- [x] Secrets scan in CI (Gitleaks — `.github/workflows/secrets-scan.yml`)
- [x] Benchmark endpoints read-only public aggregate

### Availability
- [x] Document horizontal scale path for core-api + workers (`docs/deployment/horizontal-scale.md`)
- [x] Health/readiness endpoints (`GET /ready` DB check)

---

## Phase 6 — Campus assistant (chatbot / guidance)

> Lightweight assistant for onboarding, workflow help, and score interpretation—not a general-purpose chatbot.

### Product
- [x] In-app assistant panel (student workspace tab)
- [x] Grounded answers: static FAQ + user's latest scorecard summary
- [x] Suggested actions: link to Builder, Jobs, rewrite tab (no autonomous writes)

### Security (blocking)
- [x] **Auth required** — same JWT; no anonymous LLM proxy
- [x] **Context isolation** — scorecard scoped to `user_id` in view
- [x] **Prompt injection defenses** — `guard.py` patterns + delimited LLM prompts; test coverage
- [x] **LLM keys server-side only** — `LLM_API_KEY` in env
- [x] **Logging redaction** — `log_redact.py` for audit previews
- [x] **Privacy notice** — `/privacy/assistant` + workspace panel disclosure

### Technical options (explore in order)
- [x] **RAG pipeline:** static FAQ; TF-IDF retrieval
- [x] **External LLM:** OpenAI-compatible API via httpx (optional when key set)
- [ ] **TensorFlow (optional):** embedding or re-ranker for RAG—offline index build, no training on student PII
- [ ] **Internal dev agents (Surf-like):** dev-only automation; not student runtime unless separately threat-modeled

### API
- [x] `POST /assistant/chat` — Pydantic request/response, rate limited

---

## Phase 7 — Enterprise hardening (post-bootcamp)

> Roadmap stub: `docs/roadmap/phase7-enterprise.md` (OIDC, DPDP, multi-college — not implemented)

- [ ] OAuth2/OIDC (college SSO)
- [ ] Refresh token rotation + device/session management UI
- [ ] Field-level encryption for email/phone
- [ ] mTLS service mesh or signed internal JWT between microservices
- [ ] DPDP compliance pack (retention, export, delete-my-data)
- [ ] WAF / DDoS at edge

---

## Cross-cutting — always in scope

- [ ] Swagger/OpenAPI accurate on every merged route
- [ ] RBAC on every new endpoint
- [ ] No secrets in git; `.env.example` placeholders only
- [ ] PlacementReadinessScore only in `packages/scoring/`
- [ ] No fabrication in rewriter (`unsupported_claims[]`)

---

_Updated: 2026-05-23 — Kirito security-first phases 4–7; Phase 4 is next._

*Related: [[MASTER_PLAN]] · [[05-ARCHITECTURE/security-architecture]] · [[02-PROJECTS/project-context]] · [[intel-index]]*
