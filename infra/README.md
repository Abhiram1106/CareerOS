# infra/

Infrastructure as code. Foundational/shared infra lives here; service-specific
runtime manifests (Dockerfiles) stay alongside each service in `services/*/`
per research §"Keep service runtime manifests near the service".

| Folder | Purpose | Status |
|---|---|---|
| `docker/` | Multi-service compose overrides (dev, test). The primary `docker-compose.yml` lives at repo root. | Skeleton |
| `environments/` | Dev/staging/prod overrides when we have multiple deploy targets. | Reserved |

For now, the canonical entry point is `docker-compose.yml` at the repo root.
