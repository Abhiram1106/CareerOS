# Domain modules

Each folder is one bounded context:

- `mutation/` — handlers (writes, orchestration)
- `query/` — query services (reads, DTO assembly)
- `dto/` — Pydantic request/response for this domain
- `mapper/` — entity ↔ DTO mapping
- `types/` — domain types and constants

Persistence lives in `app/adapter/db/persistence/<domain>/` (repos + views).
