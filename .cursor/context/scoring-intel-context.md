# Scoring + Intel Context — CareerOS Campus AI
# @include when working on packages/scoring/, services/match-engine/, services/intel-bench/

## PlacementReadinessScore formula (fixed until ADR changes it)

```
PlacementReadinessScore =
  0.35 × JD_Match
  0.20 × ATS_Parse_Safety
  0.20 × Evidence_Quality
  0.10 × Profile_Completeness
  0.10 × Interview_Readiness
  0.05 × Placement_Hygiene

JD_Match =
  0.35 × TFIDF_Cosine          (lexical overlap)
  0.35 × Embedding_Cosine      (semantic similarity via sentence-transformers)
  0.20 × Required_Skill_Recall (fraction of JD required skills found in resume)
  0.10 × Eligibility_Rule_Score (cgpa / branch / backlogs / grad_year rules)
```

Buckets: `0–49` high-risk | `50–69` borderline | `70–84` ready | `85–100` strong

## Single source of truth

The formula lives in `packages/scoring/` only.
`services/core-api` and `services/intel-bench` import it — never inline it.
Any weight change → update `packages/scoring/` + run regression tests + update ADR.

## ATS Parse-Safety penalties (services/ats-engine)

```
ATS_Parse_Safety = 100 - sum(penalties)
Penalties:
  -12  two-column layout
  -10  contact info in header/footer/text-box
  -10  heavy table-based layout
  -8   images/icons/logo present
  -8   scanned image with no text layer
  -6   missing standard section headings
  -5   non-standard date formats
  -5   oversized file (> 5 MB)
  -4   partial parse / missing key fields
  -4   incomplete employer or college names
```

## Intel optimization targets (Week 5)

| Workload | Baseline | Intel path | Expected gain |
|---|---|---|---|
| Embedding inference | PyTorch CPU | OpenVINO IR FP16 | 1.5×–4× |
| TF-IDF + cosine | stock sklearn | sklearnex patch | 1.5×–8× |
| KMeans cohort clustering | stock sklearn | sklearnex | 2×–8× |
| End-to-end score pipeline | mixed | selectively accelerated | 20%–80% |

## sklearnex pattern (strictly enforced)

```python
# ALWAYS before any sklearn import
from sklearnex import patch_sklearn
patch_sklearn()
# Now import sklearn estimators
from sklearn.feature_extraction.text import TfidfVectorizer
```

Never call `patch_sklearn()` after estimator instantiation — it will not take effect.

## OpenVINO pattern

```python
from openvino.runtime import Core
core = Core()
model = core.read_model("model.xml")
compiled = core.compile_model(model, "CPU")
# Measure accuracy delta before committing INT8
# If accuracy_delta > 0.01 on match quality → stay at FP16
```

## Benchmark dataset sizes

Always run at three sizes:
- small: 500 resumes, 50 JDs
- medium: 5 000 resumes, 300 JDs
- large: 20 000 resumes, 1 000 JDs

Report: p50 latency, p95 latency, throughput (resumes/hour), accuracy delta, memory MB.
Real measured numbers only — no vendor-headline figures.

## match-engine service (Week 2 — pending)

Port 8005. Will expose:
- `POST /match` — { resume_sections, jd_skills } → JD_Match sub-scores
- `POST /score` — { resume_id, jd_id } → full PlacementReadinessScore

Consumed via `services/core-api/app/services/clients.py::score_resume()`.
