from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

MATCH_BENCH = ROOT.parent / "match-engine" / "bench" / "run.py"
DEFAULT_OUT = ROOT / "results" / "benchmark_runs.json"
DOCS_OUT = ROOT.parent.parent / "docs" / "benchmarks" / "benchmark_runs.json"


def _load_match_compare() -> dict:
    docs_fallback = ROOT.parent.parent / "docs" / "benchmarks" / "match-engine-sklearnex.json"
    if docs_fallback.is_file():
        return json.loads(docs_fallback.read_text(encoding="utf-8"))
    if not MATCH_BENCH.is_file():
        return {"status": "skipped", "note": "match-engine bench not found"}
    cmd = [
        sys.executable,
        str(MATCH_BENCH),
        "--mode",
        "compare",
        "--out",
        str(ROOT / "results" / "_match_compare.json"),
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(MATCH_BENCH.parent.parent)
    subprocess.run(cmd, check=True, env=env)
    payload = json.loads((ROOT / "results" / "_match_compare.json").read_text(encoding="utf-8"))
    return payload


def _workload_row(
    *,
    workload_id: str,
    name: str,
    tool: str,
    compare: dict | None,
    status: str,
    note: str = "",
) -> dict:
    if compare and "stock" in compare and "intel" in compare:
        stock = compare["stock"]
        intel = compare["intel"]
        return {
            "id": workload_id,
            "name": name,
            "tool": tool,
            "status": status,
            "note": note,
            "baseline_p50_ms": stock.get("p50_latency_ms"),
            "intel_p50_ms": intel.get("p50_latency_ms"),
            "baseline_p95_ms": stock.get("p95_latency_ms"),
            "intel_p95_ms": intel.get("p95_latency_ms"),
            "speedup": compare.get("p50_speedup"),
            "accuracy_delta_pct": compare.get("accuracy_delta_pct", 0.0),
            "throughput_baseline_rph": stock.get("throughput_rph"),
            "throughput_intel_rph": intel.get("throughput_rph"),
            "dataset": compare.get("dataset", {}),
        }
    return {
        "id": workload_id,
        "name": name,
        "tool": tool,
        "status": status,
        "note": note or (compare.get("note") if compare else "Not measured"),
        "baseline_p50_ms": None,
        "intel_p50_ms": None,
        "baseline_p95_ms": None,
        "intel_p95_ms": None,
        "speedup": None,
        "accuracy_delta_pct": None,
        "throughput_baseline_rph": None,
        "throughput_intel_rph": None,
        "dataset": {},
    }


def run_all() -> dict:
    from workloads.openvino_probe import probe_openvino
    from workloads.sklearn_kmeans import benchmark_kmeans_compare

    match = _load_match_compare()
    kmeans = benchmark_kmeans_compare()
    openvino = probe_openvino()

    kmeans_status = "measured" if kmeans and "stock" in kmeans else "skipped"
    kmeans_note = kmeans.get("note", "") if kmeans and "stock" not in kmeans else ""

    workloads = [
        _workload_row(
            workload_id="tfidf_cosine",
            name="TF-IDF + cosine similarity (match-engine)",
            tool="sklearnex",
            compare=match if match and "stock" in match else None,
            status="measured" if match and "stock" in match else "skipped",
            note=match.get("note", "") if match and "stock" not in match else "",
        ),
        _workload_row(
            workload_id="kmeans_cohort",
            name="KMeans cohort clustering",
            tool="sklearnex",
            compare=kmeans if kmeans and "stock" in kmeans else None,
            status=kmeans_status,
            note=kmeans_note,
        ),
        {
            "id": "embedding_openvino",
            "name": "Sentence-transformer inference",
            "tool": "OpenVINO FP16",
            "status": openvino["status"],
            "note": openvino["note"],
            "baseline_p50_ms": None,
            "intel_p50_ms": None,
            "baseline_p95_ms": None,
            "intel_p95_ms": None,
            "speedup": None,
            "accuracy_delta_pct": None,
            "throughput_baseline_rph": None,
            "throughput_intel_rph": None,
            "dataset": {"devices": openvino.get("devices", [])},
        },
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "hardware": {
            "platform": platform.platform(),
            "processor": platform.processor() or "unknown",
            "python": platform.python_version(),
        },
        "methodology": {
            "baseline": "Stock sklearn / PyTorch CPU (no Intel patches)",
            "intel_path": "sklearnex.patch_sklearn() before sklearn imports; OpenVINO when IR present",
            "accuracy_guard": "If accuracy_delta > 1% vs baseline, do not promote INT8 — stay FP16",
        },
        "workloads": workloads,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="CareerOS Intel benchmark harness")
    parser.add_argument("--workload", choices=["all"], default="all")
    parser.add_argument("--size", choices=["small", "medium", "large"], default="medium")
    parser.add_argument("--out", default=str(DEFAULT_OUT))
    args = parser.parse_args()
    _ = args.size  # reserved for future dataset scaling

    result = run_all()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if out_path.resolve() != DOCS_OUT.resolve():
        DOCS_OUT.parent.mkdir(parents=True, exist_ok=True)
        DOCS_OUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
