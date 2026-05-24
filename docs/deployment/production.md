# Production Deployment — CareerOS Student AI

## Required services

- `core-api`
- `resume-parser`
- `ats-engine`
- `ai-rewriter`
- `jobs-feed`
- `postgres`
- `redis`

## Production checklist

1. `AUTO_CREATE_TABLES=false`
2. Run Alembic baseline migration (`0001_student_baseline`)
3. Configure JWT/DB/Redis secrets from secret manager
4. Enable HTTPS and secure cookie/session policy
5. Configure log aggregation and alerting
6. Validate health checks and readiness probes

## Environment hardening

- Restrict CORS to known origins
- Enforce least-privilege DB credentials
- Use managed backups and retention policy
