"""CARE-RAG Layer 3+4: Multi-index vector knowledge base using ChromaDB.

Three persistent collections:
  resume_patterns   — anonymised Interview Ready resume chunks by role
  jd_intelligence   — parsed JD keyword patterns by role family
  user_memory       — per-user resume history and accepted suggestions

ChromaDB is embedded (no separate daemon). Data persists to /app/chroma_data.
The embedder.py MiniLM model is reused for all embedding operations.
"""

from __future__ import annotations

import logging
import os
from typing import Any

log = logging.getLogger(__name__)

_CHROMA_PATH = os.getenv("CHROMA_DATA_DIR", "/app/chroma_data")

# Lazy-initialised so the module can be imported without ChromaDB installed.
_client: Any = None
_resume_col: Any = None
_jd_col: Any = None
_user_col: Any = None


def _get_client():
    global _client
    if _client is None:
        try:
            import chromadb
            _client = chromadb.PersistentClient(path=_CHROMA_PATH)
            log.info("ChromaDB initialised at %s", _CHROMA_PATH)
        except Exception as exc:
            log.warning("ChromaDB unavailable: %s — vector store disabled", exc)
            _client = False  # sentinel so we don't retry
    return _client if _client is not False else None


def _col(name: str):
    client = _get_client()
    if client is None:
        return None
    try:
        return client.get_or_create_collection(
            name=name,
            metadata={"hnsw:space": "cosine"},
        )
    except Exception as exc:
        log.warning("Cannot get collection %s: %s", name, exc)
        return None


def _embed(text: str) -> list[float]:
    from .embedder import embed_texts
    import numpy as np
    vec = embed_texts([text])[0]
    return vec.tolist()


# ── Resume Pattern Index ───────────────────────────────────────────────────────

def index_resume_pattern(
    *,
    resume_id: int,
    user_id: int,
    resume_text: str,
    role_family: str,
    quality_class: str,
    overall_score: float,
    evidence_score: float,
) -> bool:
    """Store an anonymised resume chunk in the Resume Pattern Index.

    Only called when quality_class == 'interview_ready' so the index
    contains only successful patterns.

    Returns True on success, False if ChromaDB unavailable.
    """
    col = _col("resume_patterns")
    if col is None:
        return False
    try:
        doc_id = f"resume_{resume_id}"
        # Truncate to avoid exceeding context limits
        text_chunk = resume_text[:3000]
        col.upsert(
            ids=[doc_id],
            embeddings=[_embed(text_chunk)],
            documents=[text_chunk],
            metadatas=[{
                "resume_id": resume_id,
                "user_id": user_id,
                "role_family": role_family,
                "quality_class": quality_class,
                "overall_score": overall_score,
                "evidence_score": evidence_score,
            }],
        )
        log.info("Indexed resume_id=%d role=%s score=%.1f", resume_id, role_family, overall_score)
        return True
    except Exception as exc:
        log.warning("Failed to index resume %d: %s", resume_id, exc)
        return False


def retrieve_similar_resumes(
    *,
    query_text: str,
    role_family: str = "",
    n_results: int = 5,
    min_score: float = 65.0,
) -> list[dict]:
    """Retrieve top-N Interview Ready resumes similar to the query.

    Returns list of {text, score, role_family, evidence_score} dicts.
    Empty list if ChromaDB unavailable or no results found.
    """
    col = _col("resume_patterns")
    if col is None:
        return []
    try:
        count = col.count()
        if count == 0:
            return []

        # Build where clause — only filter if we have enough documents to satisfy it
        where: dict | None = None
        if count >= n_results:
            where = {"quality_class": "interview_ready"}
            if role_family:
                where["role_family"] = role_family

        results = col.query(
            query_embeddings=[_embed(query_text[:3000])],
            n_results=min(n_results, count),
            where=where,
            include=["documents", "metadatas", "distances"],
        )
        patterns = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        dists = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(docs, metas, dists):
            # ChromaDB cosine distance: 0 = identical, 2 = opposite
            similarity = round((1 - dist / 2) * 100, 1)
            if meta.get("overall_score", 0) >= min_score:
                patterns.append({
                    "text": doc[:500],  # short excerpt for display
                    "similarity": similarity,
                    "overall_score": meta.get("overall_score", 0),
                    "evidence_score": meta.get("evidence_score", 0),
                    "role_family": meta.get("role_family", ""),
                })
        return patterns
    except Exception as exc:
        log.warning("Retrieval failed: %s", exc)
        return []


# ── JD Intelligence Index ─────────────────────────────────────────────────────

def index_jd(
    *,
    jd_id: int,
    jd_text: str,
    role: str,
    required_skills: list[str],
) -> bool:
    """Store a parsed JD in the JD Intelligence Index."""
    col = _col("jd_intelligence")
    if col is None:
        return False
    try:
        doc_id = f"jd_{jd_id}"
        text_chunk = jd_text[:2000]
        col.upsert(
            ids=[doc_id],
            embeddings=[_embed(text_chunk)],
            documents=[text_chunk],
            metadatas=[{
                "jd_id": jd_id,
                "role": role,
                "skills": ", ".join(required_skills[:20]),
            }],
        )
        return True
    except Exception as exc:
        log.warning("Failed to index JD %d: %s", jd_id, exc)
        return False


# ── User Memory Index ─────────────────────────────────────────────────────────

def store_user_signal(
    *,
    user_id: int,
    signal_type: str,   # "suggestion_accepted" | "suggestion_rejected" | "interview_received"
    scorecard_id: int,
    content: str,
) -> bool:
    """Log a user outcome signal to the User Memory Index."""
    col = _col("user_memory")
    if col is None:
        return False
    try:
        import time
        doc_id = f"signal_{user_id}_{scorecard_id}_{signal_type}_{int(time.time())}"
        col.add(
            ids=[doc_id],
            embeddings=[_embed(content[:1000])],
            documents=[content[:1000]],
            metadatas=[{
                "user_id": user_id,
                "signal_type": signal_type,
                "scorecard_id": scorecard_id,
            }],
        )
        return True
    except Exception as exc:
        log.warning("Failed to store user signal: %s", exc)
        return False


# ── Stats ─────────────────────────────────────────────────────────────────────

def get_index_stats() -> dict:
    """Return counts for each collection."""
    stats: dict = {"available": False}
    client = _get_client()
    if client is None:
        return stats
    stats["available"] = True
    for name in ("resume_patterns", "jd_intelligence", "user_memory"):
        try:
            col = client.get_or_create_collection(name)
            stats[name] = col.count()
        except Exception:
            stats[name] = 0
    return stats
