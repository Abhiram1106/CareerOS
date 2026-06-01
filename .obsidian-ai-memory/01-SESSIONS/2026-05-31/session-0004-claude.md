---
date: 2026-05-31
tool: claude-code
model: claude-sonnet-4-6
tags: [session, phase7, ci, password-reset, benchmarks, known-gaps]
type: session
links: [error-memory, active-goals, intel-index]
---

# Session 2026-05-31 (5) — Phase 7: Regression + CI + Known Gaps

← [[_INDEX]] · [[error-memory]] · [[active-goals]]

## What was done

### Phase 7 — Full regression + CI fix + known gaps

**Discrimination gate — final pass: 5/5 PASS**
```
ats_parse_safety   spread=58.9  distinct=7  PASS
evidence_quality   spread=100.0 distinct=5  PASS
interview_readiness spread=89.5 distinct=5  PASS
placement_hygiene  spread=73.0  distinct=5  PASS
profile_completeness spread=93.5 distinct=5  PASS
```

**tsc --noEmit: no errors**

---

### CI workflow fixed and expanded

**Problem:** `security-audit.yml` was failing every push because:
- `pip-audit --desc on` syntax invalid in newer pip-audit versions
- `--severity critical --fail-on critical` flags don't exist
- `torch==2.5.1+cpu` local build tag not resolvable on PyPI → audit crash

**New `ci.yml`** (5 parallel jobs):
1. `typecheck` — `tsc --noEmit` on apps/web
2. `python-syntax` — `ast.parse` all .py files (fast, no deps)
3. `python-audit` — `pip-audit --no-deps --skip-editable` with correct flags;
   match-engine filters out `torch==X+cpu` before auditing
4. `npm-audit` — `pnpm audit --audit-level critical`
5. `scoring-gate` — runs discrimination gate inline (no Docker required)
6. `docker-build` — smoke build of core-api image

**Fixed `security-audit.yml`** — correct pip-audit flags, weekly schedule,
non-critical steps `continue-on-error: true`.

---

### Password reset — console-mode (no email dependency)

New endpoints:
- `POST /auth/reset-request {email}` → prints token to server logs
- `POST /auth/reset-confirm {token, new_password}` → updates hash, revokes all sessions

New files:
- `reset_password_handler.py` — in-process token store, 30min TTL
- `user_repo.find_by_id`, `session_repo.revoke_all_for_user` — new methods
- `PasswordResetRequest`, `PasswordResetConfirm` DTOs
- `/reset-password` page — two-stage UI (request → confirm → done)
- `api.ts` — `requestPasswordReset`, `confirmPasswordReset` typed wrappers
- Login page — "Forgot password?" link replaces dead "contact placement coordinator" text

Retrieve token: `docker compose logs core-api | grep PASSWORD_RESET_TOKEN`

---

### Intel benchmark updated

`docs/benchmarks/benchmark_runs.json` now has real measured numbers for embedding:
- `embedding_minilm` workload: p50=24.37ms, p95=37.38ms, 147,729 pairs/hr (PyTorch CPU)
- Replaces old `embedding_openvino` stub (status=skipped, no data)

---

## What's left (honest remaining gaps)

| Gap | Status | Notes |
|---|---|---|
| OpenVINO IR model | Not built | Run `optimum-cli export openvino` to generate IR artifacts |
| Officer dashboard | Not built | Entire `(officer)/` route group — planned post-bootcamp |
| KMeans benchmark | Skipped | sklearnex ImportError in bench runner environment |
| `[N]%` placeholder UX | By design | Students fill in; could be improved with inline editor |

---

*Related: [[active-goals]] · [[error-memory]] · [[intel-index]]*
