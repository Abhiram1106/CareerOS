# 08 — AI & ML Stack

## Overview

CareerOS has three AI-powered subsystems:
1. **Sentence embeddings** (match-engine) — semantic JD-resume similarity
2. **Proof-linked rewriter** (ai-rewriter) — deterministic resume improvement
3. **ATS analyzer** (ats-engine / packages/scoring) — multi-signal parse-safety scoring

None of these require an external LLM API key. The system runs fully offline.

---

## 1. Sentence Embeddings (match-engine)

**Model:** `sentence-transformers/all-MiniLM-L6-v2`
- 22 MB, 384 dimensions, MIT license
- Pre-cached in Docker image at build time (`/app/.cache/huggingface`)
- No cold-start download on container start

**Backend selection** (`services/match-engine/app/embedder.py`):
```
1. OpenVINO IR at /app/model_ir/model.xml  → "sentence_embedding_openvino"
2. sentence-transformers PyTorch CPU        → "sentence_embedding"       ← active now
3. char-n-gram TF-IDF fallback             → "char_ngram_proxy"
```

The `semantic_method` field in every scorecard response reports which backend ran. Never trust the field name `embedding_cosine` alone — check `semantic_method`.

**Measured performance (Docker container, CPU):**
- p50: 24.37 ms per resume+JD pair
- p95: 37.38 ms
- Throughput: 147,729 pairs/hour

**To enable OpenVINO** (faster):
```bash
pip install optimum[openvino]
optimum-cli export openvino \
  --model sentence-transformers/all-MiniLM-L6-v2 \
  --task feature-extraction \
  services/match-engine/model_ir/
```
Then rebuild the match-engine image. The code path is already wired in `embedder.py`.

**Skill matching** (`skill_taxonomy.py`):
- 70 canonical skills + 50 aliases
- Two-pass span-claimed matching (prevents `js` matching inside `next.js`)
- Aliases: `k8s`→`kubernetes`, `ml`→`machine learning`, `nodejs`→`node.js`, etc.
- Deliberately excluded: `go` (too ambiguous), `cv` (curriculum vitae), `py` (prose)

---

## 2. Proof-Linked Rewriter (ai-rewriter)

**File:** `services/ai-rewriter/app/modules/rewrite/mutation/proof_linked_rewrite_handler.py`

**Design contract:** Never fabricate. Only strengthen what exists.

**Pipeline per bullet:**
1. Check for unsupported claims (superlatives, unanchored metrics, leadership scope) → if found, emit unchanged with conf=0.0
2. Check for weak opener (`worked on`, `helped with`, `assisted in`) → upgrade to strong verb
3. If bare bullet (no metric AND no tech term) → add `[N]% improvement` placeholder + first JD skill
4. Compute confidence from signal density (verb + metric + evidence + length)

**Filler detection:**
Strips 15 generic phrases (`team player`, `quick learner`, `self-motivated`, etc.). If result is < 6 words or broken, replaces with a placeholder prompting the student to write real content.

**ATS flag → fix mapping:**
16 flags mapped to human-readable messages + actionable fixes in `_FLAG_DETAILS` dict.

**Generate resume handler** (`generate_resume_handler.py`):
Structured template that reads `full_name`, `target_role`, `city`, `skills_csv`, `summary`, `experience_bullet`. Emits `[bracketed placeholders]` for empty fields — no boilerplate.

**Note:** The rewriter does NOT yet read from the structured `WorkExperience`/`Project` tables. That's M2 on the roadmap — it currently reads from `resume_sections` (parsed from uploaded PDF/DOCX).

---

## 3. ATS Analyzer (packages/scoring/parse_safety.py)

**Entry point:** `analyze_ats(resume_text: str, flags: list[str]) -> dict`

**7 dimensions, each scored 0–100:**

| Dimension | Key signals |
|---|---|
| contact_reachability | Email regex, Indian phone regex, LinkedIn/GitHub URL |
| section_structure | Education/Experience/Skills/Projects headings in text |
| formatting_safety | No table chars (│┌), no excessive tabs, no known image words |
| date_consistency | Mix of date formats penalised |
| content_density | Word count 150–1200 = optimal |
| bullet_structure | Action verbs, metric patterns in bullets |
| parse_cleanliness | Encoding issues, line length anomalies |

Weighted composite: `overall = Σ(weight_i × score_i)`

**Flag-only fallback:** `ats_parse_safety_from_flags(flags)` = 100 minus sum of penalties. This runs when resume_text is not available. **The scorecard handler always uses `analyze_ats`** — never the flag-only path for new code.

---

## 4. Intel Layer

**sklearnex** (`match-engine/app/intel_patch.py`):
```python
from sklearnex import patch_sklearn
patch_sklearn()  # must be before any sklearn import
```
Patches TF-IDF + cosine_similarity to use Intel-optimized BLAS routines.
Measured speedup on TF-IDF workload: **1.136×** (baseline 20.9ms → Intel 18.4ms p50).

**Benchmarks** (`docs/benchmarks/benchmark_runs.json`):
- TF-IDF cosine: **measured** (1.136× speedup, 0% accuracy delta)
- KMeans cohort: **skipped** (sklearnex ImportError in bench runner)
- MiniLM embedding: **measured** (24.37ms p50 PyTorch CPU; OpenVINO pending IR)

To re-run benchmarks:
```bash
cd services/intel-bench
python run.py --workload all --size medium
```

---

## Adding a new ML component

1. Add to the appropriate service (match-engine for scoring, ai-rewriter for generation)
2. **Never** inline model inference in core-api — always go through a service
3. Add an honest `semantic_method` or `method_label` field to the response
4. Measure it — add a workload to `services/intel-bench/workloads/`
5. Update `docs/benchmarks/benchmark_runs.json` with real numbers
