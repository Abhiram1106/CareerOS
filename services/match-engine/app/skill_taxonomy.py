"""Campus-placement skill taxonomy for JD extraction and recall."""

from __future__ import annotations

import re

# Canonical lowercase tokens; longest phrases first for regex alternation
SKILL_TAXONOMY: tuple[str, ...] = (
    "machine learning",
    "deep learning",
    "data structures",
    "object oriented programming",
    "rest api",
    "node.js",
    "react.js",
    "next.js",
    "spring boot",
    "power bi",
    "tableau",
    "communication skills",
    "problem solving",
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "angular",
    "vue",
    "django",
    "fastapi",
    "flask",
    "spring",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "ci/cd",
    "c++",
    "c#",
    ".net",
    "html",
    "css",
    "linux",
    "oop",
    "algorithms",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "excel",
    "agile",
    "scrum",
)


def _pattern_for(skill: str) -> str:
    escaped = re.escape(skill).replace(r"\ ", r"[\s\-_]+")
    return rf"\b{escaped}\b"


def extract_skills_from_text(text: str) -> list[str]:
    low = text.lower()
    found: list[str] = []
    for skill in sorted(SKILL_TAXONOMY, key=len, reverse=True):
        if re.search(_pattern_for(skill), low, re.IGNORECASE):
            found.append(skill)
    return found


def parse_required_skills_block(jd_text: str) -> list[str]:
    """Skills listed after headings like 'Required Skills' or bullet lists."""
    lines = jd_text.splitlines()
    capture = False
    block: list[str] = []
    for line in lines:
        low = line.strip().lower()
        if re.search(r"\b(required|must have|mandatory|key)\s+skills?\b", low):
            capture = True
            continue
        if capture and re.match(r"^[a-z].*:$", low) and "skill" not in low:
            break
        if capture:
            block.append(line)
    return extract_skills_from_text("\n".join(block)) if block else extract_skills_from_text(jd_text)
