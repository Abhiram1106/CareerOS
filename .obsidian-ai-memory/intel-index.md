---
tags: [hub, intel, openvino, sklearnex, benchmark, moc]
type: moc
created: 2026-05-21
updated: 2026-05-21
links: [_INDEX, MASTER_PLAN, scoring-knowledge, 02-PROJECTS/bootcamp-brief]
---

# ⚡ Intel Index — OpenVINO + sklearnex + Benchmark MOC

> Compute-layer knowledge for the Intel AI Bootcamp story.  
> **Real measured numbers only** — no vendor headline claims.

← [[_INDEX]] | [[MASTER_PLAN#Week 5]] | [[scoring-knowledge]] | [[02-PROJECTS/bootcamp-brief#The Intel integration]]

---

## Why Intel (honest story)

| Workload | Nature | Intel fit |
|----------|--------|-----------|
| TF-IDF + cosine on batches | CPU-bound linear algebra | **sklearnex** patches sklearn |
| Sentence embeddings at scale | Inference-heavy | **OpenVINO** FP16 on CPU |
| KMeans cohort analytics | Batch clustering | sklearnex KMeans |
| Benchmark harness | Compare baseline vs Intel | `services/intel-bench/` |

Judges care: measurable delta, explainable demo Scene 6 — [[02-PROJECTS/bootcamp-brief#The 3-minute demo script]]

---

## sklearnex — patch before import

```python
from sklearnex import patch_sklearn
patch_sklearn()  # FIRST — before any sklearn import
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
```

| Rule | Detail |
|------|--------|
| Order | `patch_sklearn()` must run before sklearn imports in every process |
| Where | `services/match-engine/` entrypoint, `intel-bench` harness |
| Failure mode | Silent fallback to stock sklearn — no speedup |

→ Used for JD_Match TF-IDF leg — [[scoring-knowledge#JD_Match sub-formula]]

---

## OpenVINO — embedding inference

```python
from openvino.runtime import Core
core = Core()
model = core.read_model("model/embedding_model.xml")
compiled = core.compile_model(model, "CPU")
```

| Policy | Action |
|--------|--------|
| Default precision | FP16 |
| Accuracy guard | If accuracy_delta > **1%** vs PyTorch baseline → stay FP16, document honestly |
| Do not ship INT8 | Unless delta ≤ 1% on match-quality eval set |

Feeds **Embedding_Cosine** in [[scoring-knowledge#JD_Match sub-formula]].

---

## Benchmark schema (`benchmark_runs`)

| Field | Meaning |
|-------|---------|
| `workload` | e.g. `tfidf`, `embedding`, `kmeans`, `full_pipeline` |
| `size` | `small` (500) / `medium` (5000) / `large` (20000) |
| `p50_latency_ms` | Median |
| `p95_latency_ms` | Tail |
| `throughput_rph` | Resumes per hour |
| `accuracy_delta` | vs baseline — must be < 0.01 for claims |
| `memory_mb` | Peak RSS |
| `hw_label` | Exact CPU model + RAM |
| `backend` | `baseline` \| `intel_sklearnex` \| `intel_openvino` |

**Storage:** `benchmark_runs` table · JSON artifact `services/intel-bench/results/benchmark_runs.json`  
**UI:** `apps/web/app/lab/intel/` — [[MASTER_PLAN#Week 5]]

---

## Measurement methodology

1. Run on **physical Intel hardware** (label `hw_label` in output).
2. Three dataset sizes per workload (small / medium / large).
3. Baseline: stock sklearn + PyTorch embeddings.
4. Intel: sklearnex + OpenVINO compiled model.
5. Report p50, p95, throughput, accuracy_delta, memory — no cherry-picking.

```bash
python services/intel-bench/run.py --workload all --size medium
```

→ Workflow: [[06-WORKFLOWS/README#Running the Intel benchmark]]

---

## Placeholder warning (Week 5)

Until `intel-bench` runs on target hardware:

- Lab UI may show **sample** or empty state — label clearly in demo
- Do not cite unmeasured speedup multipliers in pitch slides

---

## Service map

| Artifact | Path |
|----------|------|
| Match engine (Week 2) | `services/match-engine/` |
| Bench harness | `services/intel-bench/` |
| Scoring (consumes scores, not HW) | `packages/scoring/` |
| Officer/student UI | `/lab/intel` route |

---

## Bootcamp alignment

| Criterion | Intel evidence |
|-----------|----------------|
| Intel relevance | OpenVINO + sklearnex in critical path |
| Technical depth | Benchmark table + accuracy guard |
| Demo | Scene 6 side-by-side latency/throughput |

Full brief: [[02-PROJECTS/bootcamp-brief]] · Roadmap: [[MASTER_PLAN#Week 5]]

---

*Related: [[_INDEX]] · [[MASTER_PLAN]] · [[scoring-knowledge]] · [[architecture-index]] · [[api-index]] · [[02-PROJECTS/bootcamp-brief]] · [[06-WORKFLOWS/README]]*
