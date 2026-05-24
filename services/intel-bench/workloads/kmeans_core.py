from __future__ import annotations

import os
import random
import statistics
import time


def run_kmeans_benchmark(*, patch_intel: bool) -> dict:
    if patch_intel:
        from sklearnex import patch_sklearn

        patch_sklearn()
    else:
        os.environ["SKLEARNEX_DISABLE"] = "true"

    from sklearn.cluster import KMeans  # noqa: PLC0415
    from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: PLC0415

    random.seed(42)
    docs = [
        f"resume {i} python java sql docker kubernetes react fastapi postgres redis"
        for i in range(500)
    ]
    vectorizer = TfidfVectorizer(max_features=256)
    matrix = vectorizer.fit_transform(docs)

    latencies_ms: list[float] = []
    for n_clusters in (4, 6, 8, 10):
        for _ in range(5):
            start = time.perf_counter()
            KMeans(n_clusters=n_clusters, n_init=3, random_state=42).fit(matrix)
            latencies_ms.append((time.perf_counter() - start) * 1000)

    p50 = round(statistics.median(latencies_ms), 3)
    p95 = round(statistics.quantiles(latencies_ms, n=100)[94], 3)
    throughput_rph = round((len(latencies_ms) / sum(latencies_ms)) * 1000 * 3600, 1)
    return {
        "pairs": len(latencies_ms),
        "p50_latency_ms": p50,
        "p95_latency_ms": p95,
        "throughput_rph": throughput_rph,
    }
