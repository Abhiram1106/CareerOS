# 10 — What's Next

Full product vision: `CareerOS_Complete_Documentation.md`
CARE-RAG pipeline spec: `CareerOS_CARE_RAG_Project_Idea.md`
Internal architecture: `.obsidian-ai-memory/02-PROJECTS/care-rag-architecture.md`

---

## The bigger picture

CareerOS is now evolving from an ATS checker into **CARE-RAG** — a continuously improving AI career intelligence platform. The architecture is 7 layers. The MVP layers (1, 2 partial, 5 partial, 6 partial) are built. The RAG core (layers 3+4) and the learning loop (layer 6 full) are next.

Pick tasks in priority order below. Each one builds on the previous.

---

## M6 — 7-Class Resume Quality Classifier (IMMEDIATE — zero new infra)

**Why first:** Replaces the 4-bucket score label with a diagnostic classification that tells the student *what type of problem they have*, not just how bad the score is. Uses existing scores — no new services.

**7 classes and detection logic:**

| Class | When | Student sees |
|---|---|---|
| ATS Broken | ats_parse_safety < 40 OR table/two-column flags | "ATS cannot parse your resume — fix formatting first" |
| Structurally Weak | profile_completeness < 40 OR missing headings | "Critical sections are missing" |
| Keyword Weak | jd_match < 40 AND skill_recall < 30 | "Your skills exist but aren't in your resume" |
| Impact Weak | evidence_quality < 40 | "Add numbers and outcomes to your bullets" |
| Role Misaligned | jd_match < 35 despite ats_parse_safety > 65 | "Good resume, wrong role — tailor it" |
| High Potential, Underwritten | ats_parse_safety >= 65 AND evidence_quality < 40 | "You have the skills — your resume doesn't show it" |
| Interview Ready | overall_score >= 70 | "Strong — focus on JD-specific tailoring" |

**Where to build:**
- `packages/scoring/careeros_scoring/formula.py` — add `classify_resume_quality(scores) → str`
- `services/core-api/app/modules/scorecard/mutation/score_resume_handler.py` — inject into response
- `apps/web/app/(app)/match/page.tsx` — replace bucket badge with diagnostic class + fix guidance

---

## M7 — JD Intelligence Heatmap UI (IMMEDIATE — frontend only)

**Why:** Keyword gap analysis already returns data. This is just better UI — no backend changes needed.

**What to build in `/match` page:**
- Each JD keyword shown as a chip: green (present in resume), amber (partially present), red (missing)
- Frequency badge on each chip showing how many times it appears in the JD
- "Skill vs resume gap" label: "You have Docker but didn't mention it" vs "You don't have Docker"
- Role alignment indicator: which role family this JD matches (frontend/backend/data/devops)

**File:** `apps/web/components/workspace/KeywordHeatmap.tsx` (new), `apps/web/app/(app)/match/page.tsx`

---

## M8 — Guided AI Resume Wizard (MEDIUM — rule-based, no LLM)

**Why:** The CARE-RAG Layer 5 reasoning flow — Diagnose → Compare → Recommend → Rewrite → Verify — is the core UX differentiator. Rule-based is fine for MVP.

**5-step wizard at `/resume/wizard`:**

1. **Diagnose** — show quality_class + top 3 score gaps from latest scorecard
2. **Compare** — "Strong resumes for this role typically have..." (static role-based patterns)
3. **Recommend** — prioritised fix list with estimated Δscore per fix
4. **Rewrite** — run proof-linked rewriter on selected sections
5. **Verify** — re-score, show before/after score bars and quality_class change

**Files:** `apps/web/app/(app)/resume/wizard/page.tsx` (new), extend `services/ai-rewriter/`

---

## M9 — Vector Store + Resume Pattern Retrieval (LARGE — CARE-RAG core)

**Why this matters most:** This is the structural core of CARE-RAG. Without it, suggestions are rule-based. With it, suggestions are grounded: "78% of Interview Ready backend resumes in our knowledge base include API integration evidence."

**Architecture:**

```
services/vector-store/       ← new ChromaDB service
  app/main.py                ← FastAPI + ChromaDB
  app/indexes/
    resume_patterns.py       ← Interview Ready resume chunks by role
    jd_intelligence.py       ← JD keyword patterns by role family
    user_memory.py           ← per-user history
```

**Flow:**
1. Every scorecard with quality_class = Interview Ready → embed resume text → store in `resume_patterns`
2. Every parsed JD → embed → store in `jd_intelligence`
3. At rewrite time → retrieve top-5 similar successful resumes for same role
4. Rewriter uses retrieved patterns as grounding context
5. Every suggestion gets provenance: "Based on 12 Interview Ready {role} resumes"

**Tech:** ChromaDB (embedded, no external API, runs in-container alongside match-engine)

---

## M10 — Skill Graph Index (MEDIUM)

**Why:** Flat skill taxonomy misses relationships. "You know React" should suggest "also add JavaScript, REST API, TypeScript" — skills from the same family that JDs commonly pair together.

**Example graph:**
```
React → JavaScript → Frontend → REST API → UI Components → TypeScript
Python → Pandas → SQL → Dashboard → Data Analyst → Power BI / Tableau
Java → Spring Boot → REST API → Backend → Microservices → Docker
Docker → Kubernetes → DevOps → CI/CD → AWS/GCP/Azure
```

**Where:** Extend `services/match-engine/app/skill_taxonomy.py` with adjacency dict.
Use in keyword gap analysis: "You're missing SQL — which is 2 hops from your Python skill."

---

## M11 — Feedback Loop Wiring (MEDIUM)

**Why:** This closes the learning loop. Without it, CARE-RAG can't improve over time.

**What to wire:**
- When a recommendation is accepted → log `care_rag.suggestion.accepted` to EventAudit
- When `JobApplication.status` → `interview` or `offer` → tag source scorecard as positive outcome
- Positive-outcome scorecards populate the Resume Pattern Index (M9) preferentially
- Surface to user: "X students with similar profiles got interviews after making this change"

**What exists already:**
- `recommendations.accepted` field in DB
- `job_applications.status` workflow
- `events_audit` table

**What's missing:** The wiring logic that connects these to the vector store and surfaces the signal.

---

## M12 — Resume Evolution Timeline UI (SMALL)

**Why:** CARE-RAG §7.3 — users need to see their progress. Data already exists in score history.

**What to build:**
- Version each generated resume as v1, v2, v3... with timestamp + quality_class label
- Timeline view on `/resume` page: v1 ATS Broken → v2 Keyword Weak → v3 Interview Ready
- Before/after comparison: side-by-side score bars for any two versions
- "You improved from ATS Broken → Interview Ready in 3 edits" milestone callout

---

## Post-MVP backlog

| Item | Maps to |
|---|---|
| B2B college placement dashboard | CARE-RAG §7.6 — dept heatmaps, cohort analytics |
| LinkedIn OAuth + profile import | CARE-RAG Layer 1 ingestion |
| Google OAuth sign-in | Auth expansion |
| Job alerts + email notifications | CARE-RAG Layer 6 (outcome nudges) |
| Cover letter generator | CARE-RAG Layer 5 extension |
| Interview preparation from resume + JD | CARE-RAG §8 V3 |
| OpenVINO IR for embeddings | 2-3× faster inference |
| Learning-to-rank model | CARE-RAG V3 (train on outcome data) |
| Fine-tuned resume quality classifier | CARE-RAG V3 |
| Placement prediction | CARE-RAG V3 |

---

## Conventions for all new work

- Every new API endpoint → typed wrapper in `apps/web/lib/api.ts`
- Every scoring change → discrimination gate 5/5 must hold
- Every Python file → AST-parse clean
- Every frontend change → `tsc --noEmit` clean
- Every AI suggestion → must include `confidence`, `evidence_source` fields
- No fabrication → all suggestions go through `unsupported_claims[]` gate
- Commit vault digest after every significant session
- Commit format: `feat:` / `fix:` / `docs:` / `memory:` — one concern per commit
- CARE-RAG layer reference in commit message for M6–M12 work
