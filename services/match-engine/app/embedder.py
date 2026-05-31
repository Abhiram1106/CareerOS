"""Sentence embedding for JD-resume semantic matching.

Provides ``embed_texts(texts)`` which returns a numpy array of shape
(N, dim). Inference backend is chosen at import time:

Priority order:
  1. OpenVINO IR model at OPENVINO_MODEL_DIR (fastest on Intel hardware)
  2. sentence-transformers PyTorch (accurate, cross-platform)
  3. char-n-gram TF-IDF proxy (no model needed — degraded mode, labelled honestly)

The active backend is exposed as ``BACKEND`` and ``SEMANTIC_METHOD`` so
callers can report which method was used without inspecting internals.
"""

from __future__ import annotations

import logging
import os
from typing import Callable

import numpy as np

log = logging.getLogger(__name__)

# ── Backend selection ────────────────────────────────────────────────────────

OPENVINO_MODEL_DIR = os.getenv("OPENVINO_MODEL_DIR", "/app/model_ir")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

BACKEND: str = "unavailable"
SEMANTIC_METHOD: str = "char_ngram_proxy"

_embed_fn: Callable[[list[str]], np.ndarray] | None = None


def _try_openvino() -> bool:
    """Attempt to load the OpenVINO IR model. Returns True on success."""
    global _embed_fn, BACKEND, SEMANTIC_METHOD
    try:
        from openvino.runtime import Core  # type: ignore[import]
        import xml.etree.ElementTree as ET

        model_xml = os.path.join(OPENVINO_MODEL_DIR, "model.xml")
        if not os.path.isfile(model_xml):
            return False

        core = Core()
        ov_model = core.read_model(model_xml)
        compiled = core.compile_model(ov_model, "CPU")
        output_layer = compiled.output(0)

        try:
            from tokenizers import Tokenizer  # type: ignore[import]
            tok_path = os.path.join(OPENVINO_MODEL_DIR, "tokenizer.json")
            tokenizer = Tokenizer.from_file(tok_path)
            tokenizer.enable_padding(length=128)
            tokenizer.enable_truncation(max_length=128)

            def _ov_embed(texts: list[str]) -> np.ndarray:
                enc = tokenizer.encode_batch(texts)
                ids = np.array([e.ids for e in enc], dtype=np.int64)
                mask = np.array([e.attention_mask for e in enc], dtype=np.int64)
                token_type = np.zeros_like(ids)
                result = compiled({
                    "input_ids": ids,
                    "attention_mask": mask,
                    "token_type_ids": token_type,
                })[output_layer]
                # Mean pool over sequence dimension
                vecs = result.mean(axis=1)
                norms = np.linalg.norm(vecs, axis=1, keepdims=True)
                return vecs / np.maximum(norms, 1e-9)

            _embed_fn = _ov_embed
            BACKEND = "openvino"
            SEMANTIC_METHOD = "sentence_embedding_openvino"
            log.info("Embedder: OpenVINO IR backend loaded from %s", OPENVINO_MODEL_DIR)
            return True
        except Exception as e:
            log.warning("OpenVINO tokenizer load failed: %s", e)
            return False
    except Exception as e:
        log.debug("OpenVINO not available: %s", e)
        return False


def _try_sentence_transformers() -> bool:
    """Attempt to load sentence-transformers PyTorch model."""
    global _embed_fn, BACKEND, SEMANTIC_METHOD
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore[import]

        _model_cache_dir = os.getenv("HF_HOME", "/app/.cache/huggingface")
        model = SentenceTransformer(MODEL_NAME, cache_folder=_model_cache_dir)
        model.eval()

        def _st_embed(texts: list[str]) -> np.ndarray:
            vecs = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
            return np.array(vecs)

        _embed_fn = _st_embed
        BACKEND = "sentence_transformers"
        SEMANTIC_METHOD = "sentence_embedding"
        log.info("Embedder: sentence-transformers PyTorch backend loaded (%s)", MODEL_NAME)
        return True
    except Exception as e:
        log.debug("sentence-transformers not available: %s", e)
        return False


def _char_ngram_fallback(texts: list[str]) -> np.ndarray:
    """Char-n-gram TF-IDF fallback — no model required."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=6000)
    mat = vec.fit_transform(texts)
    arr = mat.toarray().astype(np.float32)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    return arr / np.maximum(norms, 1e-9)


# Initialise at import time — pick best available backend.
if not _try_openvino():
    if not _try_sentence_transformers():
        _embed_fn = _char_ngram_fallback
        BACKEND = "char_ngram_fallback"
        SEMANTIC_METHOD = "char_ngram_proxy"
        log.warning(
            "Embedder: no model available — using char-n-gram TF-IDF proxy. "
            "Install sentence-transformers or provide OPENVINO_MODEL_DIR."
        )


# ── Public API ───────────────────────────────────────────────────────────────

def embed_texts(texts: list[str]) -> np.ndarray:
    """Return normalised embedding matrix (N, dim) for the given texts."""
    assert _embed_fn is not None
    return _embed_fn(texts)


def cosine_similarity_pct(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """Cosine similarity between two 1-D unit vectors → [0, 100]."""
    sim = float(np.dot(vec_a, vec_b))
    return round(max(0.0, min(100.0, sim * 100)), 1)
