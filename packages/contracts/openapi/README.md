# OpenAPI contracts

Committed OpenAPI 3.x exports for CareerOS APIs (Phase 4 deliverable).

## Purpose

- Single contract for frontend codegen, integration tests, and security review
- Complements live Swagger UI at `http://localhost:8000/docs` (FastAPI auto-schema)

## Files (planned)

| File | Service |
|------|---------|
| `core-api.openapi.json` | Orchestration API (`services/core-api`) |
| `match-engine.openapi.json` | Optional — match microservice |

## Export (maintainers)

From repo root with core-api running or via FastAPI app import:

```bash
# Example: fetch from running container
curl -s http://localhost:8000/openapi.json -o packages/contracts/openapi/core-api.openapi.json
```

CI (Phase 5): fail if `/openapi.json` drifts from committed file without version bump.

## Alignment

- Request/response shapes must match `packages/contracts/schemas/*.json`
- See `docs/adr/0007-security-first-future-phases.md` and vault `05-ARCHITECTURE/security-architecture.md`
