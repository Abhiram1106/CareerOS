# Threat Model — CareerOS Campus AI (STRIDE-lite)

> Living document for Phase 4 security gate. Expand as officer and assistant surfaces ship.  
> Full control catalog: `.obsidian-ai-memory/05-ARCHITECTURE/security-architecture.md`

## Assets

| Asset | Sensitivity |
|-------|-------------|
| Resume files and parsed sections | High (PII, employment history) |
| Scorecards and recommendations | High |
| Agent run summaries | Medium–High |
| JWT / session tokens | Critical |
| LLM API keys | Critical |
| Officer cohort aggregates | Medium (institutional) |

## Trust boundaries

```
[Browser] --TLS--> [Reverse proxy] --TLS--> [core-api] --private network--> [microservices]
                                                      |
                                                      +--> [PostgreSQL]
                                                      +--> [Redis]
```

## STRIDE summary

| Threat | Example | Mitigation (current / planned) |
|--------|---------|--------------------------------|
| **Spoofing** | Stolen JWT | Short TTL, server-side session table, logout revocation (Phase 4) |
| **Tampering** | Modify scorecard_id in URL | Ownership checks in repos (Phase 4) |
| **Repudiation** | Officer approves without trace | `events_audit` logging (Phase 4) |
| **Information disclosure** | IDOR on resume | User-scoped queries; tests (Phase 4) |
| **Denial of service** | Flood `/agent/run` | Rate limits (Phase 4) |
| **Elevation of privilege** | Student calls officer route | `require_officer` on all officer endpoints |

## Assistant-specific (Phase 6)

| Threat | Mitigation |
|--------|------------|
| Prompt injection | Locked system prompt; no privileged tools without RBAC |
| Cross-user data in RAG | Index only public docs + requesting user's artifacts |
| LLM data residency | Configurable provider; disclosure in privacy notice |

## Out of scope (MVP)

- Nation-state adversaries
- Hardware security modules (Phase 7 consideration)

## Review cadence

Update this file when adding: officer batch APIs, assistant chat, or external integrations.
