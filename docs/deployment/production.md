# Production deployment — CareerOS Campus AI

## Database schema

- Set **`AUTO_CREATE_TABLES=false`** on `core-api` and Celery workers in every production environment.
- Apply schema only with Alembic:

```bash
cd services/core-api
alembic upgrade head
```

Never rely on SQLAlchemy `create_all` in production — it bypasses migration history and can drift from `entities.py`.

## Required environment variables

| Variable | Production value |
|----------|------------------|
| `AUTO_CREATE_TABLES` | `false` |
| `JWT_SECRET` | Strong random secret (not `change-me`) |
| `DATABASE_URL` | Managed PostgreSQL URL |
| `ENABLE_OFFICER_SURFACE` | `true` only when TPO review is complete |
| `LLM_API_KEY` | Optional; leave empty for FAQ-only assistant |

## Docker Compose

Use `docker-compose.prod.yml` overlay or set in your orchestrator:

```yaml
environment:
  AUTO_CREATE_TABLES: "false"
```

Internal services (`resume-parser`, `match-engine`, `ai-rewriter`, `ats-engine`) should not publish host ports — only `core-api` and `web` are public.

## Health checks

- `GET /health` — process up
- `GET /ready` — database connectivity

## Horizontal scale (path)

- Stateless `core-api` replicas behind a load balancer
- Shared PostgreSQL + Redis
- Celery workers scaled independently for export/ATS jobs
