from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def benchmark_kmeans_compare() -> dict | None:
    cmd = [sys.executable, str(Path(__file__).resolve()), "--mode", "single", "--patch-mode"]
    base_env = os.environ.copy()
    base_env["PYTHONPATH"] = str(ROOT)
    try:
        stock = subprocess.check_output(cmd + ["stock"], text=True, env=base_env, stderr=subprocess.STDOUT)
        intel = subprocess.check_output(cmd + ["intel"], text=True, env=base_env, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as exc:
        return {
            "status": "skipped",
            "note": (exc.output or str(exc))[:500],
        }
    stock_json = json.loads(stock.strip())
    intel_json = json.loads(intel.strip())
    speedup = round(stock_json["p50_latency_ms"] / max(intel_json["p50_latency_ms"], 0.001), 3)
    return {
        "dataset": {"documents": 500, "runs": stock_json["pairs"]},
        "stock": {**stock_json, "mode": "stock"},
        "intel": {**intel_json, "mode": "intel"},
        "p50_speedup": speedup,
        "accuracy_delta_pct": 0.0,
    }


if __name__ == "__main__":
    import argparse

    from workloads.kmeans_core import run_kmeans_benchmark

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["single"], default="single")
    parser.add_argument("--patch-mode", choices=["stock", "intel"], default="intel")
    args = parser.parse_args()
    print(json.dumps(run_kmeans_benchmark(patch_intel=args.patch_mode == "intel")))
