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
    jd_eligibility: dict[str, Any] | None = None,
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

    eligibility_rule_score = _eligibility_score(student_profile or {}, jd_eligibility)

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


def _eligibility_score(profile: dict[str, Any], jd_eligibility: dict[str, Any] | None = None) -> float:
    """Real eligibility scoring against JD requirements.

    Compares student CGPA, active backlogs, branch, and graduation year from
    their profile against the parsed JD eligibility criteria. Each criterion
    that fails incurs a calibrated penalty. When the JD has no criterion (None),
    that dimension is skipped — a JD without a CGPA requirement cannot penalise
    any student on CGPA.

    Returns 0–100. 100 = fully eligible. Partial penalties allow borderline
    candidates to score higher than clearly ineligible ones.
    """
    if not profile and not jd_eligibility:
        return 100.0

    jd = jd_eligibility or {}
    score = 100.0

    # CGPA criterion
    min_cgpa = jd.get("min_cgpa")
    student_cgpa = profile.get("cgpa") if profile else None
    if min_cgpa is not None:
        if student_cgpa is None:
            score -= 10  # unknown CGPA: moderate penalty, not disqualifying
        elif student_cgpa < min_cgpa:
            gap = min_cgpa - student_cgpa
            score -= min(35.0, gap * 12)  # 1pt below → -12; 3pt below → -35 cap

    # Backlog criterion
    max_backlogs = jd.get("max_backlogs")
    student_backlogs = profile.get("active_backlogs", 0) if profile else 0
    if max_backlogs is not None:
        if student_backlogs > max_backlogs:
            excess = student_backlogs - max_backlogs
            score -= min(40.0, excess * 20)  # each extra backlog: -20, cap 40

    # Branch criterion
    allowed_branches = jd.get("allowed_branches", [])
    student_branch = (profile.get("branch", "") if profile else "").upper().replace(" ", "")
    if allowed_branches and student_branch:
        # Normalise: "CSE" matches "COMPUTERSCIENCE" etc.
        _BRANCH_ALIASES: dict[str, str] = {
            "CS": "CSE", "COMPUTERSCIENCE": "CSE",
            "INFORMATIONTECHNOLOGY": "IT",
            "ELECTRONICSANDCOMMUNICATION": "ECE",
            "ELECTRONICSANDCOMMUNICATIONENGINEERING": "ECE",
        }
        normalised = _BRANCH_ALIASES.get(student_branch, student_branch)
        if normalised not in allowed_branches:
            score -= 15

    # Graduation year criterion
    allowed_years = jd.get("graduation_years", [])
    student_year = profile.get("grad_year") if profile else None
    if allowed_years and student_year is not None:
        if student_year not in allowed_years:
            score -= 20

    return max(0.0, min(100.0, round(score, 1)))
