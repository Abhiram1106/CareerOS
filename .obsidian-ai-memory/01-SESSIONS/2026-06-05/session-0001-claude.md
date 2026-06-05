---
date: 2026-06-05
tool: claude-code
model: claude-sonnet-4-6
tags: [session, ci, care-rag, wizard, retrieval, fix]
type: session
links: [active-goals, care-rag-architecture]
---

# Session 2026-06-05 (2) — CI re-enabled + wizard real retrieval wired

## What was done

### Fix 1 — CI workflows re-enabled

All three GitHub Actions workflows restored to auto-trigger:
- `ci.yml` — push/pull_request on main (5 jobs: tsc, AST, pip-audit, scoring gate, docker build)
- `secrets-scan.yml` — push/pull_request on main (Gitleaks)
- `security-audit.yml` — push on requirements.txt changes + weekly cron Monday 03:00 UTC

### Fix 2 — Wizard Step 2 wired to CARE-RAG M9 vector store

`apps/web/app/(app)/resume/wizard/page.tsx`:

**New state:**
- `retrievedPatterns: RetrievedPattern[]` — patterns from knowledge base
- `patternsLoading: boolean` — loading indicator

**Fetch on mount:**
```
useEffect → api.similarResumes(token, roleFamily, 5)
          → setRetrievedPatterns(res.patterns)
```
Only fires when `hasScoreData` is true (wizard unlocked after JD scan).

**StepCompare updated:**
- Source badge shows KB status ("X real resumes retrieved" vs "reference patterns")
- Gap bars use KB averages when real patterns exist
- Shows up to 3 retrieved excerpts with similarity % + score badge
- Graceful fallback to static ROLE_PATTERNS when KB is empty
- Clear provenance: excerpts labelled as real resumes from the knowledge base

---

## Remaining honest gaps

| Gap | Priority |
|---|---|
| No pytest coverage on core-api handlers | Low — scoring gate covers scoring logic |
| Vector store empty until 70+ scorers exist | Self-resolving as users improve |
| B2B officer portal | Post-MVP |
| LinkedIn OAuth | Post-MVP |
| OpenVINO IR model | Post-MVP |

*Related: [[active-goals]] · [[care-rag-architecture]]*
