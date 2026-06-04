---
date: 2026-06-04
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M8, care-rag, wizard, guided-flow]
type: session
links: [active-goals, care-rag-architecture, error-memory]
---

# Session 2026-06-04 (3) — M8: Guided AI Resume Wizard

## What was done

### M8 — Guided AI Resume Wizard (CARE-RAG Layer 5)

`apps/web/app/(app)/resume/wizard/page.tsx` — new 5-step wizard at `/resume/wizard`

**Step 1 — Diagnose:**
- Quality class banner with icon + colour + actionable guidance text
- Top 3 score gap bars (evidence, jd_match, completeness, ats_safety sorted by value)
- Opportunity list: top fixes with estimated Δscore preview

**Step 2 — Compare:**
- `detectRole()` infers role family from matched skills + target role text
  (backend / frontend / data / devops / default)
- Shows typical Interview Ready scores for that role vs user's current scores
- Side-by-side bar comparison (blue = user, grey = typical)
- Example STAR bullet from a strong resume in that role family
- Keywords that strong resumes in the role typically include

**Step 3 — Recommend:**
- `buildRecommendations()` ranks fixes by estimated Δscore contribution
- Top 4 fixes shown with priority number + estimated score lift
- Evidence fix (highest delta) → "Apply Rewrite" button → jumps to Step 4
- Completeness fix → "Go to Profile" links to /settings
- Total potential gain callout

**Step 4 — Rewrite:**
- Full `RewriteDiffPanel` embedded inline
- If no bundle yet: "Run Proof-Linked Rewrite" button
- If bundle exists: shows original vs rewrite diff, unsupported claims

**Step 5 — Verify:**
- Before/after delta badge (📈 if improved, 📊 if not)
- Full `ScoreBreakdown` bars after re-scan
- Prompts user to go to /match if no new scan yet

**Progress bar:** Clickable step tabs, done steps show ✓ checkmark, active step highlighted blue

**Empty state:** When no scorecard exists yet, prompts upload + JD scan with links

**`apps/web/app/(app)/resume/page.tsx`:** "🧙 Improvement Wizard" CTA in page title row

**Role patterns (CARE-RAG Layer 3 stub):**
- 5 role families: backend, frontend, data, devops, default
- Each has: typical scores, example STAR bullet, required keyword list
- Ready to be replaced with real vector store retrieval in M9

---

## tsc: no errors
## AST: all Python files clean (no Python changes this session)

---

## Next: M9 — Vector Store + Resume Pattern Retrieval

The structural core of CARE-RAG. ChromaDB embedded in match-engine.
Every Interview Ready scorecard → embed + store in Resume Pattern Index.
At rewrite time → retrieve top-5 similar resumes → provenance-grounded suggestions.
Replaces role_patterns static dict in wizard with real retrieved examples.

*Related: [[active-goals]] · [[care-rag-architecture]]*
