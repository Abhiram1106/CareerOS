# Core API

This service runs the CareerOS orchestration API.

## Local Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Database Migrations

```bash
alembic upgrade head
```

Core API now starts in migration-first mode by default and will fail startup if DB revision is not at Alembic head.

## Seed Dev Data

```bash
python scripts/seed_dev_data.py
```

Optional overrides:

```bash
python scripts/seed_dev_data.py --email demo2@careeros.dev --password DemoPass123 --full-name "Demo User 2"
```

## Env Highlights

- `DATABASE_URL` (default `sqlite:///./careeros_dev.db`)
- `AUTO_CREATE_TABLES` (`false` by default; set to `true` only for temporary local bootstrapping)
- `EXPORTS_DIR` (default `./exports`)
- `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`, `RAZORPAY_CALLBACK_URL`
- `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_SUCCESS_URL`, `STRIPE_CANCEL_URL`
- `ALERT_DISPATCH_INTERVAL_MINUTES` (default `15`, used by Celery Beat)

## New APIs in This Phase

- `POST /billing/checkout`
- `POST /billing/webhook/{provider}`
- `POST /resumes/export`
- `GET /resumes/export/{job_id}`
- `GET /resumes/export/{job_id}/download`

`/billing/checkout` now uses real provider SDK calls:
- Razorpay Payment Link API via `razorpay` SDK
- Stripe Checkout Session via `stripe` SDK

`/billing/webhook/{provider}` now verifies signed webhooks using raw request payload:
- Razorpay: `x-razorpay-signature` with HMAC SHA-256
- Stripe: `stripe-signature` via Stripe webhook signing secret

## Resume Export Storage

Export pipeline now renders real PDFs using WeasyPrint templates.

- `EXPORT_STORAGE=local` (default): saves files under `EXPORTS_DIR`
- `EXPORT_STORAGE=s3`: uploads files to S3 and `/resumes/export/{job_id}/download` returns a signed redirect URL

Relevant env vars for S3:
- `S3_EXPORT_BUCKET`
- `S3_EXPORT_PREFIX` (default: `resume-exports`)
- `S3_REGION` (default: `ap-south-1`)
- `S3_ENDPOINT_URL` (optional, for S3-compatible stores)
- `EXPORT_SIGNED_URL_TTL_SECONDS` (default: `900`)
- `WEASYPRINT_ENABLED` (`auto` by default; uses WeasyPrint in Linux/Docker, fallback renderer on Windows unless set to `true`)

## Background Alert Dispatch

Celery Beat schedules `dispatch_job_alerts` periodically using `ALERT_DISPATCH_INTERVAL_MINUTES`.
In Docker compose, run both `core-worker` and `core-beat` services for automatic dispatch.
