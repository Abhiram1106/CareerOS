# CareerOS Implementation Tracker

This tracks execution against `CareerOS_Phasewise_Roadmap.md`.

## Phase 0: Planning and Design
- [x] Monorepo architecture scaffolded
- [x] Service boundaries defined (`web`, `core-api`, `ats-engine`, `job-intel`, `ai-inference`)
- [x] Docker Compose baseline for full stack

## Phase 1: MVP Foundation
- [x] Auth (register/login), token sessions
- [x] Career profile CRUD
- [x] Resume generation orchestration (core -> ai-inference)
- [x] ATS scan orchestration (core -> ats-engine)
- [x] Job matching orchestration (core -> job-intel)
- [x] Dashboard aggregation
- [x] Next.js frontend connected end-to-end
- [x] Payment integration layer with Razorpay/Stripe SDK wiring and signed webhooks
- [x] Billing foundation (plans + subscription APIs) with provider-backed checkout flow
- [x] Async PDF export pipeline with WeasyPrint template path + local/S3 storage
- [ ] OAuth (Google/LinkedIn)

## Phase 2: Intelligence
- [x] ATS scan history API
- [x] Job alerts CRUD API
- [x] Application tracker CRUD API
- [x] Frontend panels for alerts/history/applications
- [x] Alert dispatch worker + notifications API with Celery Beat periodic scheduling
- [ ] Analytics expansion (market intelligence)
- [ ] Resume versioning UI workflow

## Phase 3: Scale
- [ ] B2B institutional portal
- [ ] Recruiter module
- [ ] Mobile app (React Native)
- [ ] ML-assisted ATS upgrade path

## Platform Foundations
- [x] Alembic migration scaffold and initial revision
- [x] Celery fallback for local broker-less execution

## ATS Track (ATS Folder)
- [x] NEXUS ATS service scaffolded in `../ATS/nexus_ats`
- [x] Blueprint-aligned v1 APIs for requisitions, candidates, applications, interviews, scorecards, offers
- [x] AI endpoints expanded (`match`, `parse-resume`, `jd-enhance`, prediction, bias scan, rediscovery, chat)
- [x] Webhook event catalog and event emission flow
- [x] Core API proxy integration (`/nexus-ats/...`) extended for ATS endpoints

## Immediate Next Build Block
1. [x] Enforce migration-first startup (`AUTO_CREATE_TABLES=false`) and add seed scripts.
2. [x] Upgrade PDF export to WeasyPrint HTML templates and S3 object storage.
3. [x] Wire real Razorpay/Stripe SDK calls and signed webhook verification.
4. Add background alert dispatch with Celery beat.
4. [x] Add background alert dispatch with Celery beat.
