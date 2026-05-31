"""Benchmark: MiniLM sentence embedding — PyTorch CPU vs OpenVINO IR.

Measures p50/p95 latency and throughput for encoding 50 resume+JD text pairs
using ``sentence-transformers/all-MiniLM-L6-v2``.

Two paths measured:
  1. ``pytorch_cpu``   — stock PyTorch inference, no Intel patches.
  2. ``openvino_fp16`` — OpenVINO IR compiled for CPU (if model IR present).

Accuracy guard: cosine similarity between PyTorch and OpenVINO embeddings is
measured on a held-out pair. If the delta exceeds 1%, the OpenVINO workload is
marked ``accuracy_fail`` and the harness stays on PyTorch.
"""

from __future__ import annotations

import time
from pathlib import Path
from typing import Any

import numpy as np

OPENVINO_MODEL_DIR = Path("/app/model_ir")
_SAMPLE_TEXTS = [
    "Software Engineering Intern with Python FastAPI Docker Kubernetes SQL experience.",
    "Machine Learning Engineer skilled in TensorFlow PyTorch scikit-learn pandas.",
    "Full Stack Developer proficient in React TypeScript Node.js PostgreSQL.",
    "Data Analyst using Python SQL Tableau Power BI for business insights.",
    "Backend Developer with experience in Java Spring Boot microservices REST API.",
    "DevOps Engineer with CI/CD Jenkins Docker Kubernetes AWS expertise.",
    "Cloud Architect designing scalable solutions on AWS Azure GCP.",
    "Mobile Developer building iOS Android apps with Swift Kotlin Flutter.",
    "Security Engineer specialising in penetration testing SAST DAST.",
    "Data Engineer building ETL pipelines with Spark Kafka Airflow.",
]

_SAMPLE_JDS = [
    "We need a backend engineer skilled in Python, REST API, SQL, Docker.",
    "Hiring ML intern — TensorFlow, scikit-learn, pandas, Python required.",
    "Frontend role: React, TypeScript, Node.js, REST API.",
    "Data Analyst role requiring SQL, Python, Tableau, Excel.",
    "Java microservices developer, Spring Boot, REST, Docker, Kubernetes.",
]

# Repeat to reach 50 pairs
_TEXTS_50 = (_SAMPLE_TEXTS * 5)[:50]
_JDS_50 = (_SAMPLE_JDS * 10)[:50]


def _time_pytorch(n_warmup: int = 3, n_iters: int = 50) -> dict[str, Any]:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        return {"status": "skipped", "note": "sentence-transformers not installed"}

    try:
        cache = Path("/app/.cache/huggingface")
        model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            cache_folder=str(cache) if cache.exists() else None,
        )
        model.eval()

        all_texts = _TEXTS_50 + _JDS_50  # 100 texts

        # Warmup
        for _ in range(n_warmup):
            model.encode(all_texts[:10], normalize_embeddings=True, show_progress_bar=False)

        latencies: list[float] = []
        for text, jd in zip(_TEXTS_50, _JDS_50):
            t0 = time.perf_counter()
            model.encode([text, jd], normalize_embeddings=True, show_progress_bar=False)
            latencies.append((time.perf_counter() - t0) * 1000)

        arr = sorted(latencies)
        p50 = float(np.percentile(arr, 50))
        p95 = float(np.percentile(arr, 95))
        rph = round(3_600_000 / p50) if p50 > 0 else 0

        # Reference embeddings for accuracy check
        ref_vecs = model.encode(all_texts, normalize_embeddings=True, show_progress_bar=False)
        return {
            "status": "measured",
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "throughput_rph": rph,
            "ref_vecs": ref_vecs,
            "note": "",
        }
    except Exception as exc:
        return {"status": "error", "note": str(exc)}


def _time_openvino(ref_vecs: np.ndarray | None, n_warmup: int = 3) -> dict[str, Any]:
    model_xml = OPENVINO_MODEL_DIR / "model.xml"
    tok_path = OPENVINO_MODEL_DIR / "tokenizer.json"

    if not model_xml.is_file():
        return {"status": "skipped", "note": "OpenVINO IR not present at /app/model_ir/model.xml"}

    try:
        from openvino.runtime import Core
        from tokenizers import Tokenizer
    except ImportError:
        return {"status": "skipped", "note": "openvino or tokenizers package not installed"}

    try:
        core = Core()
        ov_model = core.read_model(str(model_xml))
        compiled = core.compile_model(ov_model, "CPU")
        output_layer = compiled.output(0)

        tokenizer = Tokenizer.from_file(str(tok_path))
        tokenizer.enable_padding(length=128)
        tokenizer.enable_truncation(max_length=128)

        def _infer(texts: list[str]) -> np.ndarray:
            enc = tokenizer.encode_batch(texts)
            ids = np.array([e.ids for e in enc], dtype=np.int64)
            mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
            ttype = np.zeros_like(ids)
            result = compiled({"input_ids": ids, "attention_mask": mask, "token_type_ids": ttype})[output_layer]
            vecs = result.mean(axis=1)
            norms = np.linalg.norm(vecs, axis=1, keepdims=True)
            return vecs / np.maximum(norms, 1e-9)

        all_texts = _TEXTS_50 + _JDS_50

        for _ in range(n_warmup):
            _infer(all_texts[:10])

        latencies: list[float] = []
        for text, jd in zip(_TEXTS_50, _JDS_50):
            t0 = time.perf_counter()
            _infer([text, jd])
            latencies.append((time.perf_counter() - t0) * 1000)

        arr = sorted(latencies)
        p50 = float(np.percentile(arr, 50))
        p95 = float(np.percentile(arr, 95))
        rph = round(3_600_000 / p50) if p50 > 0 else 0

        # Accuracy check vs PyTorch reference
        accuracy_delta = None
        if ref_vecs is not None:
            ov_vecs = _infer(all_texts)
            # Mean cosine similarity delta
            sims_pt = np.einsum("ij,ij->i", ref_vecs, ref_vecs)  # self-sim = 1.0
            sims_ov = np.einsum("ij,ij->i", ref_vecs, ov_vecs)
            accuracy_delta = round(float(np.mean(np.abs(1.0 - sims_ov))) * 100, 4)

        failed_accuracy = accuracy_delta is not None and accuracy_delta > 1.0

        return {
            "status": "accuracy_fail" if failed_accuracy else "measured",
            "p50_latency_ms": round(p50, 2),
            "p95_latency_ms": round(p95, 2),
            "throughput_rph": rph,
            "accuracy_delta_pct": accuracy_delta,
            "note": f"accuracy_delta {accuracy_delta}% > 1% guard — stay FP16" if failed_accuracy else "",
        }
    except Exception as exc:
        return {"status": "error", "note": str(exc)}


def benchmark_embedding_compare() -> dict[str, Any]:
    """Run PyTorch CPU baseline then OpenVINO comparison."""
    pytorch = _time_pytorch()
    ref = pytorch.pop("ref_vecs", None)
    openvino = _time_openvino(ref_vecs=ref)

    if pytorch.get("status") != "measured":
        return {"status": "skipped", "note": pytorch.get("note", "PyTorch unavailable")}

    result: dict[str, Any] = {
        "dataset": {"pairs": 50, "model": "all-MiniLM-L6-v2", "seq_len": 128},
        "pytorch_cpu": pytorch,
        "openvino": openvino,
    }

    if openvino.get("status") == "measured":
        pt_p50 = pytorch.get("p50_latency_ms", 0)
        ov_p50 = openvino.get("p50_latency_ms", 0)
        result["p50_speedup"] = round(pt_p50 / ov_p50, 3) if ov_p50 > 0 else None
        result["accuracy_delta_pct"] = openvino.get("accuracy_delta_pct")

    return result
