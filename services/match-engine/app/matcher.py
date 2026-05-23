"""TF-IDF + char n-gram cosine match (sklearnex-patched when available).

The output field ``embedding_cosine`` is intentionally named for the slot it
fills in ``packages.scoring`` — it is **not** a true sentence embedding. It is a
char-n-gram TF-IDF cosine, which is a fast lexical proxy for semantic overlap
that catches misspellings and morphological variants without any model.

When real embeddings (e.g. OpenVINO MiniLM) replace this proxy in Week 5, the
slot stays the same and only ``semantic_method`` changes from
``"char_ngram_proxy"`` to ``"sentence_embedding"``. UI tooltips read
``semantic_method`` so the user never sees a misleading "embedding" claim.
"""

from __future__ import annotations

from typing import Any

from .intel_patch import patch_sklearn_if_available

patch_sklearn_if_available()

from sklearn.feature_extraction.text import TfidfVectorizer  # noqa: E402
from sklearn.metrics.pairwise import cosine_similarity  # noqa: E402

from .skill_taxonomy import extract_skills_from_text


def _cosine_pct(vec_a, vec_b) -> float:
    sim = cosine_similarity(vec_a, vec_b)[0, 0]
    return round(max(0.0, min(100.0, sim * 100)), 1)


def compute_match(
    resume_text: str,
    jd_text: str,
    required_skills: list[str],
    student_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    resume_text = (resume_text or "").strip()
    jd_text = (jd_text or "").strip()
    if not resume_text or not jd_text:
        return {
            "tfidf_cosine": 0.0,
            "embedding_cosine": 0.0,
            "required_skill_recall": 0.0,
            "eligibility_rule_score": 100.0,
            "jd_match": 0.0,
            "missing_required_skills": required_skills,
            "matched_skills": [],
            "match_method": "lexical_dual_tfidf",
            "semantic_method": "char_ngram_proxy",
        }

    word_vec = TfidfVectorizer(ngram_range=(1, 2), max_features=8000, stop_words="english")
    word_mat = word_vec.fit_transform([resume_text, jd_text])
    tfidf_cosine = _cosine_pct(word_mat[0], word_mat[1])

    char_vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=6000)
    char_mat = char_vec.fit_transform([resume_text, jd_text])
    embedding_cosine = _cosine_pct(char_mat[0], char_mat[1])

    resume_skills = set(extract_skills_from_text(resume_text))
    if student_profile:
        csv = str(student_profile.get("skills_csv", "")).lower()
        resume_skills |= set(extract_skills_from_text(csv))

    required = [s.lower() for s in required_skills if s]
    matched = [s for s in required if s in resume_skills]
    missing = [s for s in required if s not in resume_skills]
    recall = round(100 * len(matched) / len(required), 1) if required else 100.0

    eligibility_rule_score = _eligibility_score(student_profile or {})

    jd_match = round(
        0.35 * tfidf_cosine
        + 0.35 * embedding_cosine
        + 0.20 * recall
        + 0.10 * eligibility_rule_score,
        1,
    )

    return {
        "tfidf_cosine": tfidf_cosine,
        "embedding_cosine": embedding_cosine,
        "required_skill_recall": recall,
        "eligibility_rule_score": eligibility_rule_score,
        "jd_match": jd_match,
        "missing_required_skills": missing,
        "matched_skills": matched,
        "match_method": "lexical_dual_tfidf",
        "semantic_method": "char_ngram_proxy",
    }


def _eligibility_score(profile: dict[str, Any]) -> float:
    """Placeholder until student CGPA/backlog fields exist on profile."""
    if not profile:
        return 100.0
    score = 100.0
    if not str(profile.get("skills_csv", "")).strip():
        score -= 5
    if not str(profile.get("target_role", "")).strip():
        score -= 5
    return max(0.0, min(100.0, round(score, 1)))
