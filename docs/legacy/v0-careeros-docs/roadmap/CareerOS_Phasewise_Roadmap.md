# CareerOS Phasewise Delivery Roadmap (Execution Blueprint)

This roadmap is derived from `CareerOS_Complete_Documentation.md` and converts the existing high-level phases into an execution plan from planning to scale.

## 1. Planning Assumptions

- Kickoff date assumed: 2026-05-04 (Week 1)
- Sprint cadence: 2 weeks
- Release train: monthly production releases, weekly beta drops
- Architecture baseline: Next.js + FastAPI + PostgreSQL + Redis + S3 + microservices
- AI provider strategy: Claude primary, GPT fallback, Gemini fallback
- Compliance baseline: DPDP (India) and GDPR by design from Phase 0 onward

## 2. Delivery Model (How We Execute)

- Track A: Product and UX (discovery, flows, usability)
- Track B: Platform and Core Backend (auth, profile, resume, ATS APIs)
- Track C: AI and Data Intelligence (LLM flows, ATS NLP, compatibility scoring)
- Track D: Infrastructure, Security, and DevOps (CI/CD, observability, reliability)
- Track E: Growth and Go-to-Market (pricing, onboarding funnel, beta ops)

Each phase has hard entry/exit criteria so scope does not drift.

## 3. Phasewise Roadmap

## Phase 0: Product Planning and System Design (Weeks 1-3)
Goal: Freeze scope for MVP and de-risk architecture before heavy build.

Key outcomes:
- Finalized MVP scope (P0 + selected P1 from PRD)
- UX wireframes and clickable prototype for onboarding, resume builder, ATS results, jobs list
- Service boundary decisions and API contracts (v1)
- Data model finalization and migration plan
- Security/compliance design checklist and threat model
- Cost model baseline (infra + AI API + unit economics)

Work packages:
- PRD to executable backlog breakdown (epics, stories, acceptance criteria)
- API contract draft for `auth`, `profile`, `resumes`, `ats`, `jobs`, `analytics`
- Resume template system design (ATS-safe constraints)
- ATS scoring rubric lock for v1 rule engine
- Job API licensing and legal compliance confirmation

Exit criteria:
- Signed-off architecture decision record (ADR set)
- Sprint-ready backlog for next 8 weeks
- Figma prototype validated with 8-10 representative users
- Security and compliance checklist approved

## Phase 1: MVP Foundation Build (Weeks 4-13)
Goal: Launch monetizable core with Resume Builder + ATS scoring.

Scope:
- Auth and user/account management
- Career profile engine (single source of truth)
- AI resume builder (guided + direct edit)
- 4-6 ATS-safe templates (expand to 8 by phase end)
- PDF export with strict parseability constraints
- ATS scoring engine v1 (generic + JD-specific)
- Resume upload and scoring (PDF/DOCX)
- Basic dashboard and subscription/payments

Technical milestones:
- Sprint 1-2: Core platform and profile CRUD
- Sprint 3-4: Resume editor, live preview, template engine
- Sprint 5: AI generation workflows + validation guardrails
- Sprint 6: ATS parser and weighted scoring engine
- Sprint 7: Billing, analytics basics, beta hardening

Quality gates:
- P95 resume generation <8s
- P95 ATS scan <12s
- OWASP top-10 baseline protections enabled
- 0 critical vulnerabilities at launch
- 85%+ pass rate on ATS parseability regression suite

Exit criteria:
- Closed beta (>=500 users)
- Free/Pro tier live with payment flow
- End-to-end instrumentation (errors, latency, funnel)
- Launch readiness review passed

## Phase 2: Intelligence and Retention (Weeks 14-25)
Goal: Add Job Intelligence and deepen user retention loops.

Scope:
- Multi-API job ingestion and deduplication pipeline
- Compatibility scoring (TF-IDF + skills/experience/location)
- Job alerts (email + in-app)
- Application tracker
- Resume versioning and role-specific tailoring
- Expanded analytics dashboard and market insights

Technical milestones:
- Sprint 8-9: Job ingestion + indexing + filter/search APIs
- Sprint 10: Compatibility scoring service and ranking tuning
- Sprint 11: Alerts, tracker, and notification workflows
- Sprint 12: Dashboard enhancements + ATS model refinements

Quality gates:
- P95 jobs query latency <3s
- Match quality benchmark defined and measured weekly
- Alert delivery success >98%
- Data freshness SLA validated for external APIs

Exit criteria:
- Public launch for jobs intelligence
- Weekly active usage uplift target met (define baseline in Phase 1)
- Support playbooks and runbooks in place

## Phase 3: Scale and Enterprise (Months 7-12)
Goal: Reach scale, B2B expansion, and operational maturity.

Scope:
- B2B institutional portal (placement cell workflows)
- Recruiter module (filtered candidate discovery)
- React Native app (core workflows)
- ATS intelligence upgrade path (hybrid ML assist)
- Cost and reliability optimization for 10x load

Technical milestones:
- Q1: Multi-tenant access controls + B2B admin workflows
- Q2: Recruiter-facing search and shortlisting surfaces
- Q3: Mobile app launch (profile, resume, ATS, jobs)
- Q4: Predictive ATS model pilot using collected outcome data

Quality gates:
- 99.9% uptime SLA sustained
- Scale test at 10,000+ concurrent users with error budgets
- Tenant isolation and audit logging validated
- Unit economics dashboard reviewed monthly

Exit criteria:
- First 20 institutional clients onboarded
- Recruiter pilot live
- Mobile app store release complete

## 4. Cross-Phase Critical Path

1. Profile data model finalization -> blocks resume builder and ATS
2. Resume rendering architecture -> blocks export and ATS parseability outcomes
3. ATS parser reliability -> blocks trust and monetization
4. Job API contracts/legal terms -> blocks Phase 2 launch
5. Observability/QA automation -> blocks safe scale and enterprise readiness

## 5. Team Structure Recommendation (Minimum)

- Product: 1 PM, 1 Product Designer
- Frontend: 2 engineers
- Backend/Core API: 2 engineers
- ATS/ML services: 2 engineers
- QA/Automation: 1 QA engineer
- DevOps/SRE: 1 engineer (shared)
- Growth/Ops: 1 growth lead (from late Phase 1)

## 6. Milestone Calendar (Target)

- 2026-05-04: Phase 0 start
- 2026-05-25: Phase 0 signoff
- 2026-05-26 to 2026-08-03: Phase 1 build + beta
- 2026-08-04: MVP launch window
- 2026-08-10 to 2026-11-02: Phase 2 build + launch
- 2026-11-03 onward: Phase 3 scale track

## 7. Immediate Next 14-Day Plan (Start Now)

- Finalize MVP scope lock: select exact P1 items to include in MVP
- Produce UI kit and screen-level flows for all P0 journeys
- Define v1 API contracts and publish OpenAPI draft
- Create migration set for all core tables from documentation
- Build ATS scoring test corpus (50 sample resumes + 20 JDs)
- Set up CI/CD, monitoring, and staging environment
- Prepare beta recruitment plan and success dashboard

## 8. Definition of Done Per Phase

A phase is complete only when:
- Feature scope shipped and demoable end-to-end
- NFR targets for latency/security/reliability validated
- Instrumentation and dashboards are live
- Support and incident runbooks are documented
- Product analytics confirms adoption for that phase's core use case

---

If you want, next I can convert this into a sprint-by-sprint Jira-style backlog (epics, user stories, acceptance criteria, and estimates) for Phase 0 and Phase 1.
