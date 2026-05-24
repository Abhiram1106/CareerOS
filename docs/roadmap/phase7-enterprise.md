# Phase 7 — Enterprise (post-bootcamp)

> Not in scope for the Intel bootcamp demo. Track here for TPO procurement conversations.

## Goals

1. **Identity** — College SSO (OIDC/SAML), optional SCIM provisioning for student rosters.
2. **Privacy (India)** — DPDP-aligned consent, purpose limitation, retention schedules, data-subject requests (access/erase).
3. **Operations** — Per-tenant isolation, SIEM export, SOC2-friendly audit retention.
4. **Intel** — Production OpenVINO deployment path with measured accuracy/latency SLOs.

## Planned work (stubs only)

| Epic | Deliverables |
|------|----------------|
| OIDC | IdP metadata config; role mapping `student` / `officer` / `admin`; session bridge to existing `SessionTokens` |
| DPDP | Consent banner + lawful basis per feature; export/erase jobs; officer access justification log |
| Multi-college | `college_id` on all tenant rows; officer scope from JWT claims not env default |
| Secrets | Vault/KMS for JWT and LLM keys; no secrets in compose files |

## Dependencies

- Phase 4 officer surface stable in staging with audit + rate limits (complete).
- Legal review of assistant and cohort PDF wording.

## Non-goals

- Recruiter marketplace, billing, LinkedIn scraping (see ADR-0006 student-first pivot).
