# packages/scoring/

Python package: the **PlacementReadinessScore** formula and its sub-scores.
Shared by `services/core-api` (live scoring) and `services/intel-bench`
(benchmark harness). One source of truth so a "score lift" in the demo means
the same thing as a "score lift" in the benchmark.

## Formula (research-aligned)

```
PlacementReadinessScore =
  0.35 * JD_Match
+ 0.20 * ATS_Parse_Safety
+ 0.20 * Evidence_Quality
+ 0.10 * Profile_Completeness
+ 0.10 * Interview_Readiness
+ 0.05 * Placement_Hygiene

JD_Match =
  0.35 * TFIDF_Cosine
+ 0.35 * Embedding_Cosine
+ 0.20 * Required_Skill_Recall
+ 0.10 * Eligibility_Rule_Score
```

Buckets: `0–49` high-risk · `50–69` borderline · `70–84` ready · `85–100` strong.

## Status

Skeleton. Implementation lands with Week 2 (match engine) and Week 3
(rewriter integration).
