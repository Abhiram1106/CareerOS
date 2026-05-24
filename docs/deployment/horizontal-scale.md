# Horizontal Scale Notes — Student Platform

## API scale

- Run multiple `core-api` replicas behind a load balancer.
- Keep JWT/session checks stateless at API layer, state in Postgres/Redis.
- Use connection pooling (`pool_size` and PgBouncer where applicable).

## Worker and async scale

- Scale background workers separately from API replicas.
- Isolate long-running export/agent tasks in worker queue.

## Data layer

- Add read replicas for heavy analytics/reporting workloads.
- Monitor query latency and lock contention.
