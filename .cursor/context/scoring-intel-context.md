# Scoring + Intel Context — CareerOS Student AI
# @include when working on scoring, match-engine, or intel-bench

## PlacementReadinessScore formula

```
0.35 * JD_Match
+0.20 * ATS_Parse_Safety
+0.20 * Evidence_Quality
+0.10 * Profile_Completeness
+0.10 * Interview_Readiness
+0.05 * Placement_Hygiene
```

Buckets: `0-49 high-risk`, `50-69 borderline`, `70-84 ready`, `85-100 strong`.

## Source of truth

- Score formula lives in `packages/scoring/` only.
- Consumers import it; do not duplicate weights in services.

## Intel acceleration guardrails

- Call `sklearnex.patch_sklearn()` before sklearn imports.
- Measure baseline vs Intel paths with real benchmark artifacts.
- If accuracy regression exceeds tolerance, keep safer precision path.

## Reporting discipline

- Publish only measured metrics (p50/p95, throughput, accuracy delta, memory).
- Do not use vendor headline numbers.
