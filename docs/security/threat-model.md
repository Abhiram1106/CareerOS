# Threat Model — CareerOS Campus AI (STRIDE-lite)

> Living document for the Phase 4 security gate (officer prod blocker).  
> Control catalog: `.obsidian-ai-memory/05-ARCHITECTURE/security-architecture.md`

## Assets

| Asset | Sensitivity | Notes |
|-------|-------------|--------|
| Resume files and parsed sections | High | PII, employment history |
| Scorecards and recommendations | High | Derived employability signals |
| Agent run summaries | Medium–High | May echo resume/JD text |
| JWT / session tokens | Critical | Bearer auth to core-api |
| LLM API keys | Critical | Server-side only |
| Officer cohort aggregates | Medium | Institutional; no raw resumes in heatmap APIs |
| Audit log (`events_audit`) | Medium | Actor, action, coarse payload |

## Trust boundaries

```
[Browser] --TLS--> [Reverse proxy] --TLS--> [core-api] --private network--> [microservices]
                                                      |
                                                      +--> [PostgreSQL]
                                                      +--> [Redis / Celery]
```

Students and officers share the same API host; authorization is role-based at the route layer.

## STRIDE summary

| Threat | Example | Mitigation | Status |
|--------|---------|------------|--------|
| **Spoofing** | Stolen JWT | HS256 JWT + `SessionTokens` table; logout revokes session | Implemented |
| **Spoofing** | Register as officer | `RegisterRequest` role allow-list; officer accounts seeded / admin-only in prod | Implemented |
| **Tampering** | Extra JSON fields on mutations | `StrictModel` (`extra=forbid`) on all sensitive request DTOs | Implemented |
| **Tampering** | Modify another user's `resume_id` | User-scoped repos; 404 on cross-tenant access | Implemented |
| **Repudiation** | Officer exports cohort PDF without trace | `record_audit` on officer reads/writes | Implemented |
| **Information disclosure** | IDOR on resume/scorecard | Ownership checks in query services | Implemented |
| **Information disclosure** | Cohort PDF leaks PII | PDF uses aggregates + dept buckets only | Implemented |
| **Information disclosure** | Logs contain resume text | `log_redact` on assistant/LLM paths | Implemented |
| **Denial of service** | Flood `/agent/run` or `/assistant/chat` | Rate limits (`rate_limit.py`); officer report prefix capped | Implemented |
| **Elevation of privilege** | Student calls `/officer/*` | `require_officer` on officer router | Implemented |
| **Elevation of privilege** | Student uploads batch for another college | `officer_scope` college filter on cohort queries | Implemented (single-college MVP) |

## Input validation (request bodies)

All mutation payloads that accept JSON use `app.modules.common.dto.strict.StrictModel` (`ConfigDict(extra="forbid")`):

- Auth: `RegisterRequest`, `LoginRequest`
- Resume, export, JD, scorecard, recommendation rewrite, agent run, ATS scan, profile upsert
- Assistant: `AssistantChatRequest`
- Officer: `OfficerCreateBatchRequest`

Unknown fields return **422** before handler logic runs. Regression tests: `services/core-api/tests/test_validation_strict.py`.

## Officer surface

| Flow | Risk | Controls |
|------|------|----------|
| Dashboard / heatmap / skill gaps | Aggregate disclosure | Officer role; audit log; no per-student resume download in these endpoints |
| Batch create + multi-file upload | Malware / oversized upload | File type checks in handler; upload errors returned per file; audit on upload |
| Readiness PDF export | Mass export of cohort data | `require_officer`; rate-limit prefix `/officer/reports`; audit with byte count |
| Cohort list | Enumeration | College-scoped queries (`officer_scope`) |

**Production gate:** set `ENABLE_OFFICER_SURFACE=true` only when RBAC, audit, and rate limits are verified in staging.

## Assistant / LLM (Phase 6)

| Threat | Mitigation | Status |
|--------|------------|--------|
| Prompt injection (jailbreak, exfil) | `guard.py` pattern checks; no tool execution from chat | Implemented |
| Cross-user context in answers | Handler loads only requesting user's scorecard/resume summary | Implemented |
| LLM prompt/response in logs | Redaction helpers; FAQ fallback when no API key | Implemented |
| Fabricated placement claims | Rewriter uses `unsupported_claims[]`; scoring in `packages/scoring/` only | Implemented |

Privacy copy: `/privacy/assistant` (web) documents FAQ vs LLM modes.

## Dependency injection (testability)

Handler and query-service construction is centralized in `app/handler_dependencies.py` and re-exported from `app/dependencies.py`. Controllers use `Depends(get_*_handler)` so tests can override factories without patching route bodies.

## Authentication & sessions

| Control | Detail |
|---------|--------|
| Password storage | Hashed (bcrypt) |
| Token transport | `Authorization: Bearer` |
| Logout | Invalidates server-side session row |

## Out of scope (bootcamp MVP)

- OIDC / SAML college SSO (Phase 7)
- DPDP consent workflows and data-subject export (Phase 7)
- Field-level encryption at rest
- WAF / bot management (rely on reverse proxy in prod)

## Review cadence

Update this file when adding:

- New officer or batch APIs
- New assistant tools or RAG sources
- External integrations (webhooks, job boards)
- Auth model changes (OIDC, API keys)

**Last expanded:** Phase 4 security gate — strict DTOs, handler DI, officer/assistant controls documented.
