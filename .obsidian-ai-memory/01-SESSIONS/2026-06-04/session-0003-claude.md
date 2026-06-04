---
date: 2026-06-04
tool: claude-code
model: claude-sonnet-4-6
tags: [session, M9, care-rag, vector-store, chromadb, retrieval]
type: session
links: [active-goals, care-rag-architecture, error-memory]
---

# Session 2026-06-04 (4) — M9: CARE-RAG Vector Knowledge Base

## What was done

### M9 — Vector Store + Resume Pattern Retrieval (CARE-RAG Layers 3+4)

**`services/match-engine/app/vector_store.py`** (new):
- 3 ChromaDB persistent collections: `resume_patterns`, `jd_intelligence`, `user_memory`
- `index_resume_pattern()` — embeds + stores resume with metadata (role, quality_class, scores)
  Only called for `interview_ready` resumes — knowledge base contains only successful patterns
- `retrieve_similar_resumes()` — cosine similarity query with role_family filter
  Fixed: where clause only applied when collection has ≥ n_results entries (ChromaDB limitation)
- `index_jd()` — stores parsed JDs for JD Intelligence Index
- `store_user_signal()` — logs accepted/rejected suggestions + interview outcomes
- `get_index_stats()` — collection counts for monitoring
- Full graceful degradation: all functions return empty/False if ChromaDB unavailable

**`services/match-engine/app/main.py`:**
- 5 new `/vector/*` endpoints: index-resume, similar-resumes, index-jd, user-signal, stats

**`services/match-engine/requirements.txt`:** chromadb==0.6.3 added

**`services/match-engine/Dockerfile`:** CHROMA_DATA_DIR, mkdir at build time

**`docker-compose.yml`:** `chroma_data` named volume mounted into match-engine

**`services/core-api/app/services/clients.py`:**
- `vector_index_resume()`, `vector_similar_resumes()`, `vector_index_jd()`, `vector_user_signal()`
- All fire-and-forget, never raise (errors swallowed)

**`services/core-api/app/modules/scorecard/mutation/score_resume_handler.py`:**
- `_background_index()` async method runs after every scorecard
- JD always indexed; resume only when quality_class = interview_ready
- Uses asyncio.create_task() — non-blocking

**`services/core-api/app/api/controllers/dashboard_controller.py`:**
- `GET /analytics/similar-resumes?role_family=X&n=N` — proxies to vector store

**`apps/web/lib/api.ts`:** `api.similarResumes()` typed wrapper

---

## Verified
- ChromaDB available=True; stats endpoint live (resume_patterns/jd_intelligence/user_memory)
- JD indexed on every scorecard (jd_intelligence: 1 after scoring)
- Resume NOT indexed when quality_class=impact_weak (gate works correctly)
- Manual index + retrieval: 68.2% similarity on matching backend pattern
- tsc clean; AST clean

---

## Bug fixed during implementation
ChromaDB `col.query()` with a `where` filter fails when the collection has fewer
documents than `n_results`. Fixed: `where` clause only applied when
`col.count() >= n_results`, otherwise queries without filter.

---

## Next: M10 — Skill Graph Index

Extend `skill_taxonomy.py` with parent-child relationships:
`React → JavaScript → Frontend → REST API → UI Components`
`Python → Pandas → SQL → Dashboard → Data Analyst`

Use in keyword gap analysis: "You know Python — Pandas and SQL are 2 hops away."
Also used by wizard Step 3 (Recommend) to suggest adjacent skill additions.

*Related: [[active-goals]] · [[care-rag-architecture]]*
