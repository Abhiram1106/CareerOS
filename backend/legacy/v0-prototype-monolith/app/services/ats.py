import re


def parse_skills(skills_csv: str) -> list[str]:
    return [s.strip().lower() for s in skills_csv.split(",") if s.strip()]


def ats_scan(profile: dict, jd_text: str) -> dict:
    jd = jd_text.lower()
    skills = parse_skills(profile.get("skills_csv", ""))
    summary = (profile.get("summary") or "").lower()
    exp = (profile.get("experience_bullet") or "").lower()

    # Keyword match
    jd_tokens = set(re.findall(r"[a-zA-Z0-9\+#\.]{3,}", jd))
    resume_tokens = set(re.findall(r"[a-zA-Z0-9\+#\.]{3,}", f"{skills} {summary} {exp}"))
    overlap = len(jd_tokens.intersection(resume_tokens))
    keyword_score = min(95, max(20, overlap * 4))

    # Format score (simulated high for in-app generated profiles)
    format_score = 82

    # Quality score based on metrics / action verbs
    action_verbs = ["built", "developed", "designed", "improved", "led", "optimized", "deployed"]
    action_hits = sum(1 for v in action_verbs if v in exp)
    metric_hits = len(re.findall(r"\b\d+(%|x|k|m)?\b", exp))
    quality_score = min(95, 55 + action_hits * 5 + metric_hits * 6)

    # Completeness score
    required_fields = [
        profile.get("full_name"),
        profile.get("city"),
        profile.get("target_role"),
        profile.get("skills_csv"),
        profile.get("summary"),
        profile.get("experience_bullet"),
    ]
    completeness_score = round(100 * (sum(1 for f in required_fields if f) / len(required_fields)))

    # Contact score
    contact_score = 95 if profile.get("email") else 50

    composite = round(
        (keyword_score * 0.30)
        + (format_score * 0.20)
        + (quality_score * 0.20)
        + (completeness_score * 0.15)
        + (contact_score * 0.15),
        1,
    )

    return {
        "composite": composite,
        "keyword": round(keyword_score, 1),
        "format": round(format_score, 1),
        "quality": round(quality_score, 1),
        "complete": round(completeness_score, 1),
        "contact": round(contact_score, 1),
    }
