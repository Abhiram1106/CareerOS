---
tags: [architecture, security, cia, cryptography, rbac, openapi]
type: architecture
updated: 2026-05-23
links: [architecture-index, MASTER_PLAN, active-goals, api-index, layered-modules]
---

# Security Architecture — CareerOS Campus AI

← [[architecture-index]] · [[MASTER_PLAN]] · [[02-PROJECTS/active-goals]]

> **Kirito roadmap (planning name):** All **future phases** of CareerOS must treat security as a first-class deliverable—not a late audit. Every feature PR must map to CIA (confidentiality, integrity, availability) controls below.

Agents: read this file before implementing auth, APIs, officer surfaces, assistants, or infrastructure changes.

---

## 1. Security principles (CIA + foundations)

| Pillar | Definition in CareerOS | Primary controls |
|--------|------------------------|------------------|
| **Confidentiality** | Student resumes, JDs, scores, and rewrites are visible only to authorized roles and owners | TLS in transit, RBAC, row-level ownership checks, secrets out of repo, encrypted DB volumes in prod |
| **Integrity** | Scores, rewrites, and agent steps cannot be tampered with undetected | Pydantic validation, signed JWT claims, audit log (`events_audit`), immutable agent run summaries, proof-linked rewrite schema |
| **Availability** | Placement season spikes must not take down scoring/export | Health checks, Celery backpressure, Redis cache for jobs-feed, rate limits, horizontal scale path for stateless APIs |

**Cross-cutting domains (course-aligned):**

- **Cryptography** — TLS 1.2+, password hashing (bcrypt/argon2), JWT signing (HS256 min; RS256 preferred prod), optional field-level encryption for PII columns.
- **Computer networks** — reverse proxy TLS termination, private Docker network, service-to-service timeouts, no public exposure of worker/admin ports.
- **Secure system design** — least privilege, fail-closed auth, defense in depth, separation of duties (student vs officer vs admin).

---

## 2. Current security baseline (implemented)

| Control | Location | Status |
|---------|----------|--------|
| JWT Bearer auth | `services/core-api/app/services/auth.py`, `dependencies.py` | ✅ |
| Role claims (`student` / `officer` / `admin`) | JWT payload + `User.role` | ✅ |
| Route guards | `require_student`, `require_officer`, `require_admin` | ✅ Student routes gated |
| Session tokens table | `session_tokens` (persisted tokens) | ✅ |
| Input validation | Pydantic v2 DTOs in `app/modules/*/dto/` | ✅ Per domain |
| Proof-linked rewriter guardrails | `unsupported_claims[]`, JSON schema | ✅ |
| Officer surface default-off | `ENABLE_OFFICER_SURFACE`, web flag | ✅ |
| Golden-path security tests | `test_scoring_golden_path.py`, `test_agent_run_golden_path.py` | ✅ Partial |

**Gaps (must close in Phase 4–5 security track):**

- [ ] Exported OpenAPI 3.1 spec committed under `packages/contracts/openapi/` (not only `/docs` UI)
- [ ] Resource ownership: student A cannot read student B's resume/scorecard/agent run by ID
- [ ] Rate limiting / abuse protection on auth and upload endpoints
- [ ] Security headers middleware (HSTS, CSP, X-Frame-Options, etc.)
- [ ] Refresh token rotation or short-lived access + server-side revocation list
- [ ] Structured audit events for agent runs, exports, officer batch actions
- [ ] TLS everywhere in deployment docs + compose override for prod profile
- [ ] Secret management (no default `JWT_SECRET` in prod)
- [ ] SAST/dependency scan in CI

---

## 3. Authentication and authorization flows

### 3.1 Registration and login

```
Client → POST /auth/register | /auth/login
       → core-api validates credentials (Pydantic)
       → password verified with slow hash (never store plaintext)
       → issue JWT (sub=user_id, role, exp) + persist session_tokens row
       → return { access_token, token_type: "bearer", role }
Client stores token (web: secure pattern — prefer httpOnly cookie in prod; localStorage acceptable demo only)
```

### 3.2 Authenticated request

```
Client → Authorization: Bearer <token>
       → dependencies.current_user → get_user_by_token
       → 401 if missing/invalid/expired/revoked
       → require_* dependency enforces role
       → handler receives User; repos scope queries by user.id (student) or college_id (officer)
```

### 3.3 Authorization matrix (target state)

| Resource | student | officer | admin |
|----------|---------|---------|-------|
| Own resume / scorecard / agent_run | CRUD (own) | — | all |
| Batch / cohort aggregates | — | read (own college) | all |
| Jobs search | read | read | read |
| Export PDF | create (own) | — | all |
| Intel benchmark admin | — | — | read |

**Rule for agents:** Every new endpoint must declare `Depends(require_*)` AND repository methods must filter by `user_id` or `college_id`—never trust client-supplied IDs alone.

### 3.4 Session handling (requirements)

| Requirement | Implementation guidance |
|-------------|-------------------------|
| Token expiry | `JWT_EXPIRE_MINUTES` — shorten in prod (e.g. 60–120) |
| Revocation | Delete/invalidate `session_tokens` on logout; check on each request |
| Refresh (Phase 4+) | Optional `POST /auth/refresh` with rotation |
| Logout | `POST /auth/logout` invalidates server-side token |
| Demo mode | Clearly labeled; disabled in production builds |

---

## 4. API validation and OpenAPI (Swagger)

### 4.1 Standards

- **FastAPI** auto-generates OpenAPI at `/openapi.json` and Swagger UI at `/docs` per service.
- **Contract source of truth:** export and commit `packages/contracts/openapi/core-api.openapi.json` (and per-microservice specs where public).
- **JSON Schema** in `packages/contracts/schemas/` must stay aligned with OpenAPI components (CI diff check in Phase 5).
- **Validation:** all request bodies use Pydantic models; response models declared on routes (`response_model=`) to prevent accidental data leaks in OpenAPI and runtime.

### 4.2 Agent checklist for new endpoints

1. Define `*Request` / `*Response` DTO in `app/modules/<domain>/dto/`.
2. Wire route with `response_model`, correct HTTP status codes, and `Depends(require_*)`.
3. Reject unknown fields (`model_config` extra forbid where appropriate).
4. Validate file uploads: size cap, MIME allowlist, virus scan hook (Phase 5).
5. Update OpenAPI export + `api-index.md` vault entry.

### 4.3 Inter-service calls

- All outbound HTTP via `services/core-api/app/services/clients.py` (httpx).
- Timeouts on every call; no secrets in URLs.
- Phase 5+: optional mTLS or signed internal service tokens between core-api and microservices.

---

## 5. Encryption and secure communication

| Layer | Dev (Compose) | Production target |
|-------|---------------|-------------------|
| Client ↔ core-api | HTTP localhost | HTTPS behind reverse proxy (TLS 1.2+) |
| core-api ↔ Postgres | Plain on Docker network | TLS to managed Postgres; encrypted volumes |
| core-api ↔ Redis | Plain | TLS + AUTH password |
| Secrets | `.env` gitignored | Vault / cloud secret manager; never commit |
| PII at rest | Postgres volume | Encrypted disk; optional column encryption for email/phone |
| Backups | N/A | Encrypted backup storage |

**Cryptography notes for bootcamp narrative:**

- Passwords: one-way hashing only.
- JWT: signed with strong secret (≥256-bit entropy); consider asymmetric keys for multi-service verification.
- LLM API keys: server-side only; never exposed to browser.

---

## 6. Dependency injection and maintainability

CareerOS uses **FastAPI `Depends()`** as the DI container (Python analogue to autowiring):

| Concern | Pattern |
|---------|---------|
| DB session | `Depends(get_db)` |
| Current user | `Depends(current_user)` / `require_*` |
| Handlers | Injected in controllers: `handler = RunAgentHandler(db)` or factory in `dependencies.py` |
| HTTP clients | Module-level clients in `clients.py`; inject mock in tests |

**Phase 4 refactor goal:** centralize factories in `app/dependencies.py` (e.g. `get_agent_handler`) to ease testing and avoid `Handler(db)` construction in every controller.

---

## 7. Scalability and infrastructure (security-aware)

| Component | Scale pattern | Security note |
|-----------|---------------|---------------|
| core-api | Stateless replicas behind load balancer | Shared JWT secret or JWKS; sticky sessions not required |
| Celery workers | Horizontal workers | Same DB credentials via secrets; export dir isolated |
| match-engine / parser | Scale on CPU | No direct public ingress; internal network only |
| jobs-feed | Cache in Redis | Sanitize external API responses before persist |
| Postgres | Vertical + read replicas (future) | Row-level security optional for multi-tenant colleges |

**Availability controls:** Docker healthchecks (present), circuit breaker on external job API, queue depth alerts (Phase 5).

---

## 8. Future phases — security gates per phase

### Phase 4 — Officer dashboard + security hardening (required before officer GA)

**Product**

- Officer route group, batch upload, heatmap, review queue, readiness PDF.

**Security deliverables (blocking)**

- [ ] Ownership checks on all student resources (IDOR tests)
- [ ] Officer scoped to `college_id` / batch membership
- [ ] Audit log entries: batch create, approve, return, export
- [ ] OpenAPI export committed; Swagger documents officer routes
- [ ] Rate limits on login, upload, agent run
- [ ] Security headers middleware
- [ ] Threat model doc (STRIDE-lite) in `docs/security/threat-model.md`

### Phase 5 — Intel lab + production posture

**Product**

- `intel-bench`, `/lab/intel`, pitch deck, screenshots.

**Security deliverables**

- [ ] CI: `pip-audit` / `npm audit` (high severity fail)
- [ ] Prod compose profile: TLS, secrets, `AUTO_CREATE_TABLES=false`
- [ ] Pen-test checklist for demo environment
- [ ] DPDP-oriented data retention doc (design level)

### Phase 6 — Campus assistant (chatbot / guidance)

**Product**

- Lightweight in-app assistant: onboarding, "how to improve score," FAQ on readiness workflow—not unbounded general chat.

**Security deliverables**

- [ ] Assistant service isolated (`services/assistant/` or module in core-api)
- [ ] Auth required; scope context to user's own data only
- [ ] Prompt injection defenses: system prompt lock, no tool execution without RBAC
- [ ] RAG corpus: static docs + user's own scorecard summary (no other students' data)
- [ ] External LLM via env (`LLM_PROVIDER`, `LLM_API_KEY`); log redaction
- [ ] Optional: TensorFlow / embedding model for retrieval — run offline batch index, no training on user PII

**Architecture options (feasibility)**

| Option | Pros | Cons |
|--------|------|------|
| External API (Claude, DeepSeek, etc.) | Fast to ship | Data leaves campus boundary — disclose in privacy doc |
| Local small model (Ollama) | Confidentiality | Ops burden |
| RAG over `docs/` + vault summaries | Grounded answers | Index build pipeline |

**Surf / internal agent tooling:** evaluate for **dev-only** workflow automation (repo maintenance), not student-facing runtime unless hardened.

### Phase 7 — Enterprise hardening (post-bootcamp)

- OAuth2/OIDC for college SSO
- Field-level encryption for sensitive columns
- WAF + DDoS protection
- Formal SOC2-style control mapping (aspirational)

---

## 9. Agent implementation rules (non-negotiable)

1. **Never** commit secrets, JWT defaults, or API keys.
2. **Never** add a route without RBAC dependency appropriate to persona.
3. **Never** return full ORM entities—use response DTOs.
4. **Always** validate input with Pydantic; **always** document in OpenAPI.
5. **Always** add a test that proves 403/401 for wrong role or other user's ID.
6. **Always** log security-relevant actions to `events_audit` when touching Phase 4+ officer/batch flows.
7. Intel benchmarks must be **measured**, not claimed—same honesty standard as security.

---

## 10. Related repository paths

| Path | Purpose |
|------|---------|
| `services/core-api/app/dependencies.py` | Auth dependencies |
| `services/core-api/app/services/auth.py` | JWT + passwords |
| `services/core-api/app/models/entities.py` | Users, session_tokens, events_audit |
| `packages/contracts/schemas/` | JSON Schema contracts |
| `docs/adr/0007-security-first-future-phases.md` | ADR for this roadmap |

---

*Last updated: 2026-05-23 — Kirito / security-first future phases.*
