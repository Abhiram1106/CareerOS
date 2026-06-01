# 09 — Testing & CI

## What exists

| Test type | Where | What it checks |
|---|---|---|
| Discrimination gate | `tests/golden/_runner.py` | 5 scoring sub-scores produce differentiated output across 7 personas |
| Sub-score correctness | `tests/golden/_audit_phase4.py` | 21 specific range assertions on scoring functions |
| Extractor unit tests | `services/resume-parser/tests/test_extractor.py` | Section extraction + confidence scoring |
| TypeScript | `apps/web/` | `tsc --noEmit` clean |
| Python AST | CI only | `ast.parse` all .py files |
| pip-audit | CI + weekly | No critical CVEs in requirements.txt files |

No pytest test suite yet for core-api handlers — that's a known gap.

---

## Running tests locally

### Discrimination gate (most important)
```bash
# Copy corpus and runner into core-api container, then run
docker compose cp tests/golden/corpus.py core-api:/tmp/corpus.py
docker compose cp tests/golden/_runner.py core-api:/tmp/_runner.py
docker compose exec core-api python /tmp/_runner.py
```

Expected output — all PASS:
```
ats_parse_safety    spread=58.9  distinct=7  PASS
evidence_quality    spread=100.0 distinct=5  PASS
interview_readiness spread=89.5  distinct=5  PASS
placement_hygiene   spread=73.0  distinct=5  PASS
profile_completeness spread=93.5 distinct=5  PASS
DISCRIMINATION GATE PASSED: every sub-score discriminates.
```

### Sub-score audit
```bash
docker compose cp tests/golden/_audit_phase4.py core-api:/tmp/_audit_phase4.py
docker compose exec core-api python /tmp/_audit_phase4.py
# Expected: PHASE 4 AUDIT PASSED — all sub-score ranges correct
```

### Resume parser unit tests
```bash
docker compose exec resume-parser python -m pytest /app/test_extractor.py -v
# Expected: 5 passed
```

### TypeScript
```bash
cd apps/web && npx tsc --noEmit
# Expected: TypeScript: No errors found
```

### Python AST parse
```bash
find services packages -name "*.py" | while read f; do
  python -c "import ast; ast.parse(open('$f').read())" || echo "FAIL: $f"
done
```

---

## CI pipeline (`.github/workflows/ci.yml`)

5 jobs run on every push to `main`:

| Job | What it does | Blocks merge? |
|---|---|---|
| `typecheck` | `tsc --noEmit` | Yes |
| `python-syntax` | `ast.parse` all .py files | Yes |
| `python-audit` | pip-audit on all requirements.txt files | Yes (core-api only) |
| `npm-audit` | `pnpm audit --audit-level critical` | No (continue-on-error) |
| `scoring-gate` | Discrimination gate inline (no Docker) | Yes |
| `docker-build` | Smoke build of core-api image | Yes |

Also: `.github/workflows/security-audit.yml` runs weekly on dependency file changes.

---

## Test corpus (`tests/golden/corpus.py`)

7 personas with `text` (full resume string) and `sections` (structured section list):

| Persona | Tier | Key characteristics |
|---|---|---|
| `strong_fullstack` | strong | 2 internships, metrics, Python/Docker/K8s, GitHub |
| `strong_data` | strong | ML internships, publications, scikit-learn/TF |
| `mid_average` | mid | 1 intern, no metrics, Java/HTML/MySQL |
| `mid_nometrics` | mid | 1 intern, no metrics, Python/Flask, has GitHub |
| `weak_sparse` | weak | No contact, minimal text, coursework only |
| `weak_nocontact` | weak | No email/phone, vague prose |
| `weak_walloftext` | weak | Filler phrases, no bullets, no tech skills |

**When to update the corpus:**
- Adding a new persona: make sure the new persona changes at least one PASS/FAIL result to confirm it adds signal
- Changing scoring thresholds: re-run gate, update expectations if intentional

---

## Adding a new scoring test

1. Add a case to `tests/golden/_audit_phase4.py` with `(label, sections, expected_lo, expected_hi)`
2. Run the audit locally — confirm PASS
3. If gate is failing after a scoring change, that's a regression — fix the scorer, not the test

---

## What's NOT tested (known gaps)

- core-api handler unit tests (no pytest for auth, profile, scorecard handlers)
- integration test: full upload → score → rewrite pipeline end-to-end via HTTP
- frontend component tests
- match-engine embedding quality regression test

The discrimination gate is the primary safety net for scoring changes. For API changes, manual curl/PowerShell tests are used.
