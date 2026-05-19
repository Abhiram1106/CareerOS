# tests/

Cross-domain end-to-end and system tests only. Per-service unit tests live
next to the code (e.g. `services/core-api/tests/`, `apps/web/__tests__/`).

Reserved for:
- E2E happy-path: student loop (upload → parse → score → rewrite → export)
- E2E officer loop: batch upload → dashboard → review queue → readiness PDF
- Performance/resilience sweeps invoked from CI

Empty for now. First fixture lands with Week 2 (match engine + scorecard).
