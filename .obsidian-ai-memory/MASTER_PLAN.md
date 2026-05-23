---
tags: [hub, mission, roadmap, bootcamp, moc, security]
type: hub
created: 2026-05-21
updated: 2026-05-23
links: [_INDEX, scoring-knowledge, intel-index, architecture-index, session-index, security-architecture]
---

# MASTER_PLAN — CareerOS Campus AI

> **Mission:** Production-grade placement-readiness platform for Indian colleges — Intel-accelerated, security-first, demoable end-to-end.  
> **Positioning:** *The placement-readiness operating layer for Indian colleges.*

← [[_INDEX]] | [[architecture-index]] | [[05-ARCHITECTURE/security-architecture]] | [[scoring-knowledge]]

---

## Kirito roadmap (security-first future phases)

All work from **Phase 4 onward** follows [[05-ARCHITECTURE/security-architecture]]:

- **Confidentiality** — TLS, RBAC, ownership checks, secrets hygiene  
- **Integrity** — Pydantic validation, audit logs, proof-linked outputs  
- **Availability** — health checks, queues, rate limits, scale-out path  

Repo ADR: `docs/adr/0007-security-first-future-phases.md` · Goals: [[02-PROJECTS/active-goals]]

---

## The problem we solve

| Pain | Today | CareerOS |
|------|-------|----------|
| Resume review | WhatsApp + Excel | Parse → score → proof-linked rewrite → export |
| Company matching | Manual JD comparison | Structured JD match + readiness formula |
| Cohort intel | No visibility | Officer heatmaps (Phase 4) |
| AI trust | Black boxes | Evidence IDs; unsupported claims refused |
| Compute | Generic cloud | sklearnex + OpenVINO (measured) |

**Not:** job board · LinkedIn scraper · recruiter marketplace · unsafe AI resume spam.

---

## Roadmap status (2026-05-23)

```
Phase 0–3 ✅  Foundation, scoring, rewriter, student-first agent
Phase 4  🔨  Officer dashboard + security hardening (CURRENT)
Phase 5  ⏳  Intel lab UI + production CI/security gates
Phase 6  ⏳  Campus assistant (RAG + optional LLM)
Phase 7  ⏳  Enterprise SSO, encryption, compliance
```

### Completed highlights

- Monorepo, Alembic, JWT + RBAC, resume parser, match-engine, scoring package  
- Proof-linked rewriter, recommendations, PDF export  
- Jobs feed, deterministic agent, Builder/Jobs UI  
- sklearnex benchmark (documented), enterprise README, ADR 0006  

→ Detail: [[02-PROJECTS/active-goals]] · Sessions: [[session-index]]

### Phase 4 — Officer + security (next)

Product: officer routes, batch analytics, review queue.  
**Security gate:** IDOR tests, OpenAPI export, rate limits, audit log, threat model — see [[05-ARCHITECTURE/security-architecture#8. Future phases — security gates per phase]].

### Phase 5 — Intel + production posture

Product: intel-bench service, `/lab/intel`, pitch deck.  
Security: CI audits, prod secrets, no default JWT.

### Phase 6 — Assistant

Product: onboarding + guidance chatbot.  
Tech: RAG over docs; optional external LLM (server-side keys); optional TensorFlow retrieval; Surf-like tooling **dev-only** unless hardened.

### Phase 7 — Enterprise

OAuth/OIDC, mTLS, DPDP pack, WAF.

---

## Architecture (summary)

```
apps/web → core-api (:8000) → microservices (parser, ATS, match, rewriter, jobs-feed)
                          → PostgreSQL + Redis/Celery
```

Full diagrams: [[05-ARCHITECTURE/README]] · Security flows: [[05-ARCHITECTURE/security-architecture]]

---

## 3-minute demo (student-first)

1. Upload resume → Jobs search → Run agent  
2. Show score breakdown + rewrite diff (`unsupported_claims`)  
3. Export PDF → Intel benchmark numbers (measured)  

→ [[docs/pitch/demo-script]] (repo)

---

## Bootcamp scoring narrative

| Criterion | Angle |
|-----------|--------|
| Problem | Employability gap + ATS + TPO manual ops |
| Intel | sklearnex on match path; OpenVINO planned with accuracy gate |
| Technical depth | Multi-service, Alembic, agent state machine, RBAC |
| Security | CIA roadmap, OpenAPI, production-oriented Phase 4–7 |
| Social impact | Indian campus placement at scale |

---

## Personas

**Priya** (student) → `/workspace`, Jobs, Builder, agent  
**Mr. Ramesh** (TPO) → `/officer` (Phase 4, flag-gated)  
**Dr. Mehta** (admin) → cohort reports

---

*Related: [[_INDEX]] · [[05-ARCHITECTURE/security-architecture]] · [[02-PROJECTS/active-goals]] · [[intel-index]] · [[02-PROJECTS/bootcamp-brief]]*
