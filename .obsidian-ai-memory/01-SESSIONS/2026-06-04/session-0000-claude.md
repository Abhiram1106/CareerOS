---
date: 2026-06-04
tool: claude-code
model: claude-sonnet-4-6
tags: [session, care-rag, roadmap, architecture, planning]
type: session
links: [active-goals, care-rag-architecture, project-context]
---

# Session 2026-06-04 — CARE-RAG Integration Planning

## What was done

### Context
User presented `CareerOS_CARE_RAG_Project_Idea.md` — a specification for evolving CareerOS from
an ATS checker into a continuously improving RAG-powered career intelligence platform (CARE-RAG).

Instruction: adapt it into the existing project, not replace — keep all existing milestones.

### Analysis performed
Mapped every CARE-RAG layer against what's already built:

**Already built and mapping cleanly:**
- Layer 1 (Ingestion): resume parser, JD parser, structured profile — solid
- Layer 2 (Quality): 6-component scoring, vendor simulation, keyword gap — partial
- Layer 5 (Recommendations): proof-linked rewriter, anti-fabrication — partial
- Layer 6 (Outcomes): JobApplication tracker, score history — partial
- Layer 7 (Guardrails): confidence scores, unsupported_claims[] — partial

**Gap analysis — what CARE-RAG wants that doesn't exist:**
- Multi-index vector knowledge base (Resume Patterns, JD Intelligence, Outcome, Skill Graph, User Memory)
- Hybrid retrieval (semantic + BM25 + skill graph + outcome-based)
- 7-class diagnostic quality classifier (vs current 4 buckets)
- Provenance-based suggestions ("78% of strong resumes include X")
- Skill graph relationships (React→JavaScript→Frontend)
- Feedback loop wiring (accepted suggestions → knowledge base)
- Resume evolution timeline UI

### Documents updated

**Vault:**
- `.obsidian-ai-memory/02-PROJECTS/active-goals.md` — full rewrite with M6–M12 CARE-RAG milestones
- `.obsidian-ai-memory/02-PROJECTS/care-rag-architecture.md` — new, layer-by-layer architecture map
- `.obsidian-ai-memory/02-PROJECTS/project-context.md` — updated with CARE-RAG positioning

**Repo:**
- `docs/handoff/10-whats-next.md` — updated with M6–M12 task breakdown + CARE-RAG layer references
- `CareerOS_CARE_RAG_Project_Idea.md` — source document (already committed)

---

## The adapted roadmap

### Immediate (zero new infra)
- **M6** — 7-class resume quality classifier (deterministic from existing scores)
- **M7** — JD intelligence heatmap UI (keyword gap data already returned)

### Short-term (rule-based, no vector store)
- **M8** — Guided AI resume wizard (Diagnose→Compare→Recommend→Rewrite→Verify, 5 steps)

### Medium-term (new infra — CARE-RAG core)
- **M9** — ChromaDB vector store + multi-index knowledge base + hybrid retrieval + provenance
- **M10** — Skill graph relationships in skill_taxonomy.py
- **M11** — Feedback loop wiring (accepted suggestions → outcome → knowledge base)

### Small (data already exists)
- **M12** — Resume evolution timeline UI (version labels + before/after comparison)

### Kept from previous plan
- B2B officer portal — Post-MVP
- LinkedIn OAuth — Post-MVP
- OpenVINO IR embeddings — Post-MVP

---

## Key insight: build order matters

1. M6+M7 first — they use existing data, surface immediately in UI, unblock M8
2. M8 next — the wizard UX is the product's face; works without vector store
3. M9 is the moat — vector store + retrieval is what makes it a CARE-RAG platform not just an ATS checker
4. M11 only after M9 — feedback loop needs a knowledge base to feed into
5. College dashboard only after M11 — needs aggregated outcome data to show real patterns

---

*Related: [[active-goals]] · [[care-rag-architecture]] · [[project-context]]*
