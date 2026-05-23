from __future__ import annotations

import argparse
import json
import os
import random
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RESUME_SKILLS = [
    "python",
    "fastapi",
    "sql",
    "java",
    "spring",
    "react",
    "typescript",
    "docker",
    "kubernetes",
    "aws",
    "redis",
    "postgresql",
    "git",
    "linux",
]


def _sample_resume(i: int) -> str:
    skills = random.sample(RESUME_SKILLS, 6)
    return (
        f"Candidate {i} worked on backend APIs and production systems. "
        f"Skills: {', '.join(skills)}. "
        f"Built services, improved query latency, and participated in sprint delivery."
    )


def _sample_jd(i: int) -> str:
    required = random.sample(RESUME_SKILLS, 4)
    optional = random.sample(RESUME_SKILLS, 3)
    return (
        f"Company: CampusCo {i}\n"
        f"Role: Software Engineer\n"
        f"Required skills: {', '.join(required)}\n"
        f"Optional skills: {', '.join(optional)}\n"
        "Need API development, SQL optimization, and collaboration in agile teams."
    )


def _run_single(patch_mode: str) -> dict:
    if patch_mode == "stock":
        os.environ["SKLEARNEX_DISABLE"] = "true"
    else:
        os.environ.pop("SKLEARNEX_DISABLE", None)

    from app.jd_parser import parse_jd  # noqa: PLC0415
    from app.matcher import compute_match  # noqa: PLC0415

    random.seed(42)
    resumes = [_sample_resume(i) for i in range(50)]
    jds = [_sample_jd(i) for i in range(50)]
    parsed = [parse_jd(jd) for jd in jds]

    latencies_ms: list[float] = []
    for resume_text in resumes:
        for jd_text, parsed_jd in zip(jds, parsed):
            start = time.perf_counter()
            compute_match(resume_text, jd_text, parsed_jd.get("required_skills", []), {})
            elapsed = (time.perf_counter() - start) * 1000
            latencies_ms.append(elapsed)

    p50 = round(statistics.median(latencies_ms), 3)
    p95 = round(statistics.quantiles(latencies_ms, n=100)[94], 3)
    throughput_rph = round((len(latencies_ms) / sum(latencies_ms)) * 1000 * 3600, 1)
    return {
        "mode": patch_mode,
        "pairs": len(latencies_ms),
        "p50_latency_ms": p50,
        "p95_latency_ms": p95,
        "throughput_rph": throughput_rph,
    }


def _run_compare() -> dict:
    cmd = [sys.executable, str(Path(__file__).resolve()), "--mode", "single", "--patch-mode"]
    base_env = os.environ.copy()
    base_env["PYTHONPATH"] = str(ROOT)

    stock = subprocess.check_output(cmd + ["stock"], text=True, env=base_env)
    intel = subprocess.check_output(cmd + ["intel"], text=True, env=base_env)

    stock_json = json.loads(stock.strip())
    intel_json = json.loads(intel.strip())
    speedup = round(stock_json["p50_latency_ms"] / max(intel_json["p50_latency_ms"], 0.001), 3)
    return {
        "dataset": {"resumes": 50, "jds": 50},
        "stock": stock_json,
        "intel": intel_json,
        "p50_speedup": speedup,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Match-engine benchmark harness")
    parser.add_argument("--mode", choices=["compare", "single"], default="compare")
    parser.add_argument("--patch-mode", choices=["stock", "intel"], default="intel")
    parser.add_argument("--out", default="", help="Optional file path to write JSON output")
    args = parser.parse_args()

    result = _run_compare() if args.mode == "compare" else _run_single(args.patch_mode)
    output = json.dumps(result, indent=2)
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
