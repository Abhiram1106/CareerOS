# Deploy CareerOS to Render

This repository includes a Render Blueprint at `render.yaml` that provisions the full stack:

- `careeros-web` (Next.js)
- `careeros-core-api` (FastAPI)
- `careeros-core-worker` (Celery worker)
- `careeros-ats-engine` (private service)
- `careeros-ai-rewriter` (private service)
- `careeros-resume-parser` (private service)
- `careeros-match-engine` (private service)
- `careeros-jobs-feed` (private service)
- `careeros-db` (PostgreSQL)
- `careeros-redis` (Render Key Value)

## 1. Prepare your repository

1. Push this repo (including `render.yaml`) to GitHub.
2. Make sure your default branch is up to date.

## 2. Create services from Blueprint

1. Open Render Dashboard.
2. Click `New` -> `Blueprint`.
3. Select your GitHub repository.
4. Render will detect `render.yaml` and show all resources.
5. Choose plans (upgrade from free where needed) and create.

## 3. Sync worker secret

`careeros-core-worker` has `JWT_SECRET` with `sync: false` by design.

After the Blueprint is created:

1. Open `careeros-core-api` -> `Environment` and copy `JWT_SECRET`.
2. Open `careeros-core-worker` -> `Environment` and set `JWT_SECRET` to the same value.
3. Save and redeploy `careeros-core-worker`.

## 4. Verify service health

Check:

- `careeros-core-api/health` returns `{ "status": "ok" }`
- `careeros-core-api/ready` returns `status=ready`
- `careeros-web` loads and calls the API successfully

## 5. Frontend API URL

The blueprint sets:

- `NEXT_PUBLIC_CORE_API_URL=https://careeros-core-api.onrender.com`

If your API gets a different URL, update this variable in `careeros-web` and redeploy it.

## 6. Optional production variables

Set these only if you use those features:

- `LLM_API_KEY`, `LLM_API_BASE`, `LLM_MODEL`
- `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` (on `careeros-jobs-feed`)
- S3 export vars if switching from local export storage:
  - `EXPORT_STORAGE=s3`
  - `S3_EXPORT_BUCKET`, `S3_REGION`, optional `S3_ENDPOINT_URL`

## Notes

- Core API startup runs `alembic upgrade head` before booting Uvicorn.
- `AUTO_CREATE_TABLES` is disabled on Render (`false`) to enforce migration-first startup.
- `jobs-feed` image now includes `seed/` so fallback job results work without volume mounts.
