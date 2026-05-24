# Horizontal scale path — core-api + workers

## Current shape (bootcamp)

- **core-api:** stateless FastAPI replicas behind a load balancer
- **core-worker:** Celery workers consuming Redis broker
- **PostgreSQL:** single primary (readiness data, scorecards, batches)
- **Redis:** broker + optional cache

## Scale-out steps

1. **API tier** — run N identical `core-api` containers; sticky sessions not required (JWT is stateless).
2. **Workers** — scale `core-worker` replicas; ensure idempotent tasks and `db.close()` in `finally` (already required).
3. **Rate limits** — replace in-process `RateLimitMiddleware` with Redis-backed counters when N > 1.
4. **Exports** — use `EXPORT_STORAGE=s3` so PDF jobs from any worker write to shared object storage.
5. **DB** — connection pool per replica (`pool_size` / PgBouncer); read replicas optional for officer dashboards later.

## Health checks for orchestrators

- Liveness: `GET /health`
- Readiness: `GET /ready` (Postgres ping)

## What not to scale independently (yet)

- `resume-parser`, `match-engine`, `ai-rewriter`, `ats-engine` — internal HTTP only; scale via more core-api traffic, not public replicas.
