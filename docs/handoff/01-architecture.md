# 01 — System Architecture

## Service map

```
Browser / apps/web (:3000)
         │  HTTP
         ▼
core-api (:8000)  ←── JWT auth on every request
         │
         ├──► resume-parser (:8004)   pdfplumber + python-docx + OCR
         ├──► match-engine  (:8005)   TF-IDF + MiniLM embeddings
         ├──► ats-engine    (:8001)   parse-safety analyzer
         ├──► ai-rewriter   (:8003)   proof-linked rewriter
         └──► jobs-feed     (:8006)   Adzuna API + seed fallback
                │
         PostgreSQL (:5432)  Redis (:6379)
         └── all persistent data    └── Celery queue + cache
```

All inter-service calls go through `services/core-api/app/services/clients.py` using `httpx`. **Never** call other services directly from a controller.

---

## Services and responsibilities

### `core-api` (:8000)
The only public-facing service. Handles:
- Auth (JWT + SessionTokens table)
- Career profile CRUD (basic + structured sections)
- Resume lifecycle (upload trigger, section storage, export job queue)
- Scorecard computation (orchestrates match-engine + scoring formula)
- Recommendations (orchestrates ai-rewriter)
- Jobs (proxies jobs-feed)
- Dashboard, analytics
- Agent runs (automated parse → score → rewrite pipeline)

### `resume-parser` (:8004)
- Input: PDF or DOCX file bytes
- Output: `{sections: [...], ats_flags: [...], full_text: str, char_count: int}`
- Uses pdfplumber for native PDFs, pytesseract OCR fallback for scanned
- Section extractor uses heading heuristics + alias map (EDUCATION, EXPERIENCE, SKILLS, PROJECTS, etc.)
- Confidence derived from section richness, not hardcoded

### `match-engine` (:8005)
- Input: `{resume_text, jd_text, required_skills, student_profile}`
- Output: `{tfidf_cosine, embedding_cosine, required_skill_recall, eligibility_rule_score, jd_match, semantic_method}`
- `embedding_cosine`: MiniLM all-MiniLM-L6-v2 (384-dim, pre-cached at build)
- `semantic_method`: `"sentence_embedding"` | `"sentence_embedding_openvino"` | `"char_ngram_proxy"`
- sklearnex patches sklearn at startup for Intel-accelerated TF-IDF

### `ats-engine` (:8001)
- Input: `{resume_text?, ats_flags: [...]}`
- Output: `{ats_parse_safety, bucket, checks: [...], issues: [...]}`
- 7 dimensions: contact, section_structure, formatting, date_consistency, content_density, bullet_structure, parse_cleanliness
- Flag-based path (legacy) + full text-analysis path (`analyze_ats`)

### `ai-rewriter` (:8003)
- Input: `{resume_json, jd_json, evidence_json, ats_flags}`
- Output: `{top_issues, section_rewrites, unsupported_claims, requires_confirmation}`
- Deterministic, rule-based — no LLM call
- Verb upgrades, filler removal, STAR strengthening
- Unsupported bullets (superlatives, unanchored metrics, leadership scope) emitted unchanged with conf=0.0

### `jobs-feed` (:8006)
- Input: `?q=role&loc=city&page=N`
- Output: paged job listings
- Tries Adzuna API (if `ADZUNA_APP_ID` + `ADZUNA_APP_KEY` set), falls back to 12 seed jobs

### `packages/scoring`
Shared Python package. **PlacementReadinessScore is only ever computed here.**
```
overall = 0.35×jd_match + 0.20×ats_safety + 0.20×evidence + 0.10×completeness + 0.10×interview + 0.05×hygiene
jd_match = 0.35×tfidf + 0.35×embedding + 0.20×skill_recall + 0.10×eligibility
```

---

## Ports

| Service | Internal port | Host-exposed |
|---|---|---|
| core-api | 8000 | ✅ 0.0.0.0:8000 |
| ats-engine | 8001 | ❌ internal only |
| ai-rewriter | 8003 | ❌ internal only |
| resume-parser | 8004 | ❌ internal only |
| match-engine | 8005 | ✅ 0.0.0.0:8005 |
| jobs-feed | 8006 | ✅ 0.0.0.0:8006 |
| postgres | 5432 | ❌ internal only |
| redis | 6379 | ❌ internal only |
| frontend | 3000 | ✅ (pnpm dev) |

---

## Data flow: student uploads resume and gets score

```
1. Frontend POST /resumes/upload (multipart PDF)
2. core-api → resume-parser: parse file → sections + ats_flags + full_text
3. core-api stores: Resume row (content_text=full_text) + ResumeSection rows
4. core-api returns ParseResult to frontend

5. Frontend POST /scorecards/score {resume_id, jd_text}
6. core-api fetches resume sections → reconstructs resume_text
7. core-api → match-engine: {resume_text, jd_text, required_skills, profile}
8. match-engine returns: {tfidf_cosine, embedding_cosine, recall, eligibility, jd_match}
9. core-api calls packages/scoring: all 6 sub-scores + overall
10. core-api stores Scorecard row
11. Returns ScorecardScoreResponse to frontend
```

---

## Environment variables (key ones)

| Var | Service | Default | Notes |
|---|---|---|---|
| `DATABASE_URL` | core-api | postgres://careeros:... | Set in docker-compose |
| `REDIS_URL` | core-api | redis://redis:6379 | Set in docker-compose |
| `JWT_SECRET` | core-api | (required) | Set in .env |
| `ADZUNA_APP_ID` | jobs-feed | "" | Leave blank → seed data |
| `ADZUNA_APP_KEY` | jobs-feed | "" | Leave blank → seed data |
| `OPENVINO_MODEL_DIR` | match-engine | /app/model_ir | Set to enable OpenVINO |
| `HF_HOME` | match-engine | /app/.cache/huggingface | Pre-cached in image |
| `NEXT_PUBLIC_CORE_API_URL` | frontend | http://localhost:8000 | In apps/web/.env.local |
