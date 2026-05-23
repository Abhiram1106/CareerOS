# Match Engine Benchmark — sklearnex vs stock sklearn

Date: 2026-05-23  
Harness: `services/match-engine/bench/run.py`  
Dataset: 50 resumes x 50 JDs (2,500 match calls)  
Output JSON: `docs/benchmarks/match-engine-sklearnex.json`

## Measured results

| Metric | Stock sklearn | sklearnex | Delta |
|---|---:|---:|---:|
| p50 latency (ms) | 20.878 | 18.381 | 1.136x faster |
| p95 latency (ms) | 29.978 | 25.968 | lower tail latency |
| Throughput (resumes/hour equivalent) | 163465.5 | 202625.7 | +23.96% |

## Reproduce

From `services/match-engine`:

```bash
python bench/run.py --mode compare --out "c:/Users/ADMIN/Desktop/Projects/CareerOS/docs/benchmarks/match-engine-sklearnex.json"
```

## Notes

- `sklearnex.patch_sklearn()` is applied before sklearn imports (`app/main.py` and `app/matcher.py` import path).
- If this benchmark does not improve on a target machine, keep stock sklearn and report the measurement honestly.
- OpenVINO INT8 remains optional and is gated by an accuracy-delta threshold (<=1% vs baseline). If the delta exceeds 1%, stay on FP16.
