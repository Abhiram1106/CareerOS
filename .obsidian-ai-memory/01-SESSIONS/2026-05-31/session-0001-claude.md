---
date: 2026-05-31
tool: claude-code
model: claude-sonnet-4-6
tags: [session, phase3, embeddings, minilm, sentence-transformers, intel-bench, openvino]
type: session
links: [error-memory, active-goals, scoring-knowledge, intel-index]
---

# Session 2026-05-31 (2) — Phase 3: Real sentence embeddings

← [[_INDEX]] · [[error-memory]] · [[active-goals]] · [[intel-index]]

## What was done

### Phase 3 — Real MiniLM sentence embeddings replacing char-ngram proxy

**Problem being solved:**
The `embedding_cosine` slot in `JD_Match` was filled by char-n-gram TF-IDF — a
lexical proxy that only measures character-level overlap, not semantic meaning.
"Python developer" and "software engineer building with Python" would score
differently even though semantically equivalent. The slot was labelled
"embedding_cosine" but was not an embedding.

**Solution:**
Added `services/match-engine/app/embedder.py` — a backend-selection module that
picks the best available inference path at import time:
1. OpenVINO IR (fastest, requires `/app/model_ir/` artifacts)
2. sentence-transformers PyTorch CPU (accurate, cross-platform) ← **active now**
3. char-n-gram TF-IDF fallback (no model, labelled honestly)

Model: `sentence-transformers/all-MiniLM-L6-v2` — 22 MB, 384-dim, proven quality.

**Key design decisions:**
- Model weights baked into Docker image at build time (no cold-start HuggingFace hit)
- `SEMANTIC_METHOD` string exposed from embedder — propagated through API response
  so UI always shows the true backend, never a misleading label
- Fallback chain degrades honestly; if sentence-transformers unavailable, char-ngram
  fires and `semantic_method` reports `"char_ngram_proxy"` not `"sentence_embedding"`

---

### Files changed

| File | Change |
|---|---|
| `services/match-engine/app/embedder.py` | New — backend selector, embed_texts(), cosine_similarity_pct() |
| `services/match-engine/app/matcher.py` | embedding_cosine uses embed_texts(); semantic_method from SEMANTIC_METHOD |
| `services/match-engine/requirements.txt` | + torch==2.5.1 (CPU), sentence-transformers==3.3.1, tokenizers==0.21.0 |
| `services/match-engine/Dockerfile` | + libgomp1, CPU-only torch install, HF model pre-cache at build time |
| `services/intel-bench/workloads/embedding_minilm.py` | New — MiniLM PyTorch CPU benchmark; OpenVINO comparison with accuracy delta guard |
| `services/intel-bench/run.py` | Wires embedding_minilm workload; replaces openvino_probe stub |
| `apps/web/components/workspace/ScoreBreakdown.tsx` | Added sentence_embedding_openvino label; removed "Week 5" future-state tooltip |
| `apps/web/components/intel/IntelScoreFormulaPanel.tsx` | Formula now reads "MiniLM sentence embeddings" (accurate) |

---

### Verified measurements (this machine, Docker container)

```
MiniLM all-MiniLM-L6-v2, PyTorch CPU, 50 resume+JD pairs:
  p50 latency:  25.5 ms
  p95 latency:  33.4 ms
  throughput:   140,988 pairs/hr
  model dim:    384
```

Semantic discrimination test:
- Related pair (Python backend JD + resume): 61.0/100
- Unrelated pair (Python backend + watercolor painting): 3.7/100
- Ratio: 16× — strongly discriminating

End-to-end scorecard: `semantic_method: sentence_embedding` confirmed in API response.

---

### Discrimination gate
**5/5 PASS** — no regressions from embedding swap.

---

### Image size delta
- Before: careeros-match-engine 1.07 GB
- After: careeros-match-engine 2.53 GB (+1.46 GB = torch + model weights)

---

## What's next

- **Phase 5** — constrained LLM rewriter with anti-fabrication gate (replace regex
  string-manipulation "rewriter" with actual LLM call + unsupported_claims enforcement)
- **Phase 6** — frontend honesty + continuity fixes
- **Phase 7** — full regression + benchmark docs update

---

*Related: [[intel-index]] · [[scoring-knowledge]] · [[error-memory]] · [[active-goals]]*
