# packages/contracts/

Cross-language contracts. The **only** sanctioned way to share data shapes
between `services/` (Python) and `apps/web` (TypeScript) and any future Go/Java
services.

## Layout

```
contracts/
  openapi/          # FastAPI-emitted specs (services/core-api/docs/openapi.json etc.)
  schemas/          # Hand-authored JSON Schema for domain entities
```

## Domain schemas (Week 1–2 deliverables)

- `resume.schema.json` — parsed resume JSON: sections (`summary`, `education`,
  `experience`, `projects`, `skills`, `por`, `certifications`, `links`), each
  with `content`, `confidence`, `evidence_ids`.
- `jd.schema.json` — parsed job description: `company`, `role`, `required_skills`,
  `nice_to_have_skills`, `eligibility` (cgpa, branches, backlogs, grad_year).
- `scorecard.schema.json` — the 6-component PlacementReadinessScore output.
- `rewrite.schema.json` — the AI rewriter response: `section_rewrites`,
  `unsupported_claims`, `requires_confirmation` (research §"Output schema").

## Codegen

TypeScript types regenerate from `schemas/` into `packages/ts-types/`. Python
side uses Pydantic models that mirror the schemas (no codegen needed — types
are hand-maintained against the schema in `services/core-api/app/schemas/`).
