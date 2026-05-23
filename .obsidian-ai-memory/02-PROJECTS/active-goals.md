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
- [ ] `apps/web/(officer)/` — dashboard, batches, JDs, review queue
- [ ] Batch upload, dept heatmap, skill-gap chart, company-fit columns
- [ ] Readiness PDF report export for TPO
- [ ] Enable officer surface only after review: `ENABLE_OFFICER_SURFACE=true`

### Security (blocking)
- [ ] **IDOR prevention:** resume/scorecard/agent_run/export scoped to `user_id` or officer `college_id`
- [ ] **OpenAPI:** export `packages/contracts/openapi/core-api.openapi.json`; document all officer routes in Swagger
- [ ] **API validation:** Pydantic `extra=forbid` on sensitive DTOs; file upload size/MIME limits
- [ ] **Rate limiting:** auth, upload, `/agent/run` (Redis or middleware)
- [ ] **Security headers:** HSTS, CSP, X-Content-Type-Options, frame deny
- [ ] **Audit log:** `events_audit` for batch create, approve/return, export, officer login
- [ ] **Session hardening:** logout revokes `session_tokens`; document prod token TTL
- [ ] **DI cleanup:** handler factories in `dependencies.py` for testability
- [ ] **Tests:** 401/403 matrix per role; cross-user access must fail
- [ ] **Threat model:** `docs/security/threat-model.md` (STRIDE-lite)

### Infrastructure
- [ ] Prod compose profile: TLS termination notes, secrets via env (no defaults)
- [ ] Internal-only ports for parser/match/rewriter (no host publish except core-api/web)

---

## Phase 5 — Intel lab + production posture

### Product
- [ ] `services/intel-bench` — OpenVINO + sklearnex full harness
- [ ] `apps/web/lab/intel` — p50/p95/throughput/accuracy-delta panel
- [ ] 6-slide pitch deck, product screenshots

### Security (blocking)
- [ ] CI dependency audit (`pip-audit`, `pnpm audit`) — fail on critical
- [ ] `AUTO_CREATE_TABLES=false` in prod documentation; Alembic-only schema
- [ ] Secrets scan in CI (no keys in diff)
- [ ] Benchmark endpoints admin-only or read-only public aggregate

### Availability
- [ ] Document horizontal scale path for core-api + workers
- [ ] Health/readiness endpoints for orchestration (K8s-ready pattern)

---

## Phase 6 — Campus assistant (chatbot / guidance)

> Lightweight assistant for onboarding, workflow help, and score interpretation—not a general-purpose chatbot.

### Product
- [ ] In-app assistant panel (student workspace)
- [ ] Grounded answers: product docs + user's own latest scorecard summary
- [ ] Suggested actions: link to Builder, Jobs, rewrite tab (no autonomous writes without confirm)

### Security (blocking)
- [ ] **Auth required** — same JWT; no anonymous LLM proxy
- [ ] **Context isolation** — never inject another user's resume/score into prompt
- [ ] **Prompt injection defenses** — fixed system prompt; tool calls RBAC-gated
- [ ] **LLM keys server-side only** — `LLM_PROVIDER`, `LLM_API_KEY` in env
- [ ] **Logging redaction** — no PII in application logs
- [ ] **Privacy notice** — third-party LLM disclosure if external API used

### Technical options (explore in order)
- [ ] **RAG pipeline:** index `docs/` + static FAQ; retrieval via embeddings (TF-IDF or small embedding model)
- [ ] **External LLM:** Claude / DeepSeek / OpenAI-compatible API via httpx in `services/assistant/`
- [ ] **TensorFlow (optional):** embedding or re-ranker for RAG—offline index build, no training on student PII
- [ ] **Internal dev agents (Surf-like):** dev-only automation; not student runtime unless separately threat-modeled

### API
- [ ] `POST /assistant/chat` — Pydantic request/response, OpenAPI documented, rate limited

---

## Phase 7 — Enterprise hardening (post-bootcamp)

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
