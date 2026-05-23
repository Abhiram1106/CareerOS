"""Heuristic sub-scores from structured resume sections (Week 2 baseline)."""

from __future__ import annotations

import json
import re
from typing import Any


def resume_text_from_sections(sections: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for sec in sections:
        name = sec.get("section_name", "")
        content = sec.get("content_json", {})
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError:
                content = {"raw": content}
        raw = ""
        if isinstance(content, dict):
            raw = str(content.get("raw", ""))
        parts.append(f"{name}\n{raw}")
    return "\n".join(parts)


def _section_text(sections: list[dict[str, Any]], name: str) -> str:
    for sec in sections:
        if sec.get("section_name") == name:
            content = sec.get("content_json", {})
            if isinstance(content, str):
                try:
                    content = json.loads(content)
                except json.JSONDecodeError:
                    return content
            if isinstance(content, dict):
                return str(content.get("raw", ""))
    return ""


def evidence_quality_score(sections: list[dict[str, Any]]) -> float:
    exp = _section_text(sections, "experience").lower()
    proj = _section_text(sections, "projects").lower()
    text = f"{exp} {proj}"
    if not text.strip():
        return 35.0

    action_verbs = ["built", "developed", "designed", "implemented", "led", "optimized", "deployed", "created"]
    actions = sum(1 for v in action_verbs if v in text)
    metrics = len(re.findall(r"\b\d+(%|x|k|m|l)?\b", text))
    base = 45 + actions * 6 + metrics * 5
    return max(0.0, min(100.0, round(base, 1)))


def profile_completeness_score(sections: list[dict[str, Any]]) -> float:
    expected = ["summary", "education", "experience", "projects", "skills"]
    present = sum(1 for name in expected if _section_text(sections, name).strip())
    return round(100 * present / len(expected), 1)


def interview_readiness_score(sections: list[dict[str, Any]]) -> float:
    exp = _section_text(sections, "experience")
    proj = _section_text(sections, "projects")
    por = _section_text(sections, "positions_of_responsibility")
    depth = len(exp.split()) + len(proj.split()) + len(por.split())
    if depth < 20:
        return 40.0
    if depth < 80:
        return 62.0
    return min(95.0, 55 + depth // 10)


def placement_hygiene_score(sections: list[dict[str, Any]], ats_flags: list[str]) -> float:
    text = resume_text_from_sections(sections).lower()
    score = 88.0
    if "no_email_found" in ats_flags:
        score -= 15
    if not re.search(r"\b(education|experience|skills)\b", text):
        score -= 10
    if len(text) < 200:
        score -= 12
    return max(0.0, min(100.0, round(score, 1)))
