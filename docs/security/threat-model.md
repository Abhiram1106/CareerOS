# Threat Model — CareerOS Student AI (STRIDE-lite)

## Assets

| Asset | Sensitivity | Notes |
|---|---|---|
| Resume text + parsed sections | High | Personal data and career history |
| Scorecards + recommendations | Medium | Derived decision data |
| Session tokens | High | Account control surface |
| Audit events | Medium | Security and traceability evidence |

## Trust boundaries

1. Browser to API
2. API to database/redis
3. API to internal services
4. Assistant prompt/response boundary

## STRIDE summary

| Category | Threat | Mitigation |
|---|---|---|
| Spoofing | Token misuse | JWT validation + active session token checks |
| Tampering | Payload manipulation | Strict DTO validation (`extra=forbid`) |
| Repudiation | Untraceable actions | `events_audit` logging |
| Information disclosure | Cross-user data leak | Ownership checks on resume/export/agent routes |
| Denial of service | Endpoint flooding | Route-level rate limiting |
| Elevation of privilege | Non-student access paths | Student-only runtime gates |

## Assistant-specific controls

- Prompt-injection guardrails
- Source-grounded answer preference
- Sensitive operations require authenticated context

## Operational checklist

- Rotate secrets
- Enforce HTTPS and secure cookie settings
- Keep dependency and image patching cadence
- Monitor auth failures and rate-limit breaches
