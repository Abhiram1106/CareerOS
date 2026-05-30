"""Campus-placement skill taxonomy for JD extraction and recall.

Two mechanisms for matching:
1. SKILL_TAXONOMY — canonical lowercase tokens matched via word-boundary regex.
2. SKILL_ALIASES — maps non-canonical variants to a canonical taxonomy token,
   so "js" → "javascript", "k8s" → "kubernetes", etc. This prevents false-zero
   recall when a JD uses an abbreviation the taxonomy doesn't list.
"""

from __future__ import annotations

import re

# Canonical lowercase tokens; longest phrases first for regex alternation.
SKILL_TAXONOMY: tuple[str, ...] = (
    "machine learning",
    "deep learning",
    "data structures",
    "object oriented programming",
    "natural language processing",
    "computer vision",
    "rest api",
    "restful api",
    "graphql",
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
    "golang",
    "rust",
    "kotlin",
    "swift",
    "react",
    "angular",
    "vue",
    "django",
    "fastapi",
    "flask",
    "spring",
    "express",
    "sql",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "elasticsearch",
    "kafka",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "terraform",
    "git",
    "github",
    "gitlab",
    "ci/cd",
    "jenkins",
    "c++",
    "c#",
    ".net",
    "html",
    "css",
    "linux",
    "bash",
    "shell scripting",
    "oop",
    "algorithms",
    "tensorflow",
    "pytorch",
    "keras",
    "scikit-learn",
    "pandas",
    "numpy",
    "excel",
    "agile",
    "scrum",
    "jira",
    "microservices",
    "system design",
)

# Alias map: non-canonical form (lowercase) → canonical token in SKILL_TAXONOMY.
# Handles abbreviations, alternate spellings, and common shorthand.
#
# Rules for safe aliases:
#   - Single letters (C, R, Go) are NOT listed — too many false positives.
#   - Two-letter abbreviations: ml/dl are safe and included; cv is NOT (= curriculum vitae).
#   - Aliases that are substrings of longer taxonomy tokens are handled in
#     extract_skills_from_text via longest-match priority, not string substitution.
SKILL_ALIASES: dict[str, str] = {
    # JavaScript / TypeScript — multi-char only, safe word boundaries
    "js": "javascript",
    "ts": "typescript",
    "node": "node.js",       # "node" alone is reliably technical in resume/JD contexts
    "nodejs": "node.js",
    "node js": "node.js",
    "nextjs": "next.js",
    "next js": "next.js",
    "reactjs": "react",
    "react js": "react",
    # Python — 2-char, only safe in code/skill contexts (requires surrounding digits or comma)
    # "py" omitted — too short, false positives in prose
    # Java / Spring
    "springboot": "spring boot",
    "spring-boot": "spring boot",
    # DevOps
    "k8s": "kubernetes",
    "kube": "kubernetes",
    "cicd": "ci/cd",
    "ci cd": "ci/cd",
    "continuous integration": "ci/cd",
    "continuous deployment": "ci/cd",
    # Cloud
    "amazon web services": "aws",
    "google cloud platform": "gcp",
    "google cloud": "gcp",
    "microsoft azure": "azure",
    # Databases
    "postgres": "postgresql",
    "psql": "postgresql",
    "mongo": "mongodb",
    # ML / AI — ml/dl are safe two-letter abbreviations in tech resume contexts;
    # 'cv' is NOT included (ambiguous with curriculum vitae).
    "ml": "machine learning",
    "dl": "deep learning",
    "nlp": "natural language processing",
    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    # Go — "go" alone is too ambiguous; "golang" is already in taxonomy directly
    # "go" omitted — false positive in natural prose ("let me go", "go to")
    # API
    "restful api": "rest api",
    "restful": "restful api",
    # OOP
    "object oriented": "object oriented programming",
    "oops": "oop",
    # Data structures
    "dsa": "data structures",
    # Shell
    "bash scripting": "shell scripting",
    "linux scripting": "shell scripting",
    # Other
    "microservice": "microservices",
}


def _pattern_for(skill: str) -> str:
    """Word-boundary-safe pattern that handles special characters in skill names.

    Standard \\b fails around punctuation like +, ., /. We use negative
    lookbehind/lookahead for word characters instead for those cases.
    """
    escaped = re.escape(skill).replace(r"\ ", r"[\s\-_]+")
    # If the skill contains non-word chars at start/end, use lookaround instead of \\b
    if re.search(r"[^\w]", skill[0]) or re.search(r"[^\w]", skill[-1]):
        return rf"(?<!\w){escaped}(?!\w)"
    return rf"\b{escaped}\b"


# Pre-compile taxonomy and alias patterns for performance.
_TAXONOMY_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(_pattern_for(skill), re.IGNORECASE), skill)
    for skill in sorted(SKILL_TAXONOMY, key=len, reverse=True)
]

_ALIAS_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    (re.compile(_pattern_for(alias), re.IGNORECASE), canonical)
    for alias, canonical in sorted(SKILL_ALIASES.items(), key=lambda kv: len(kv[0]), reverse=True)
]


def extract_skills_from_text(text: str) -> list[str]:
    """Extract canonical skill tokens from free text.

    Strategy: longest-match priority to prevent short aliases from firing inside
    longer compound tokens. Aliases are checked independently (not via string
    substitution) to avoid corrupting multi-part skill names.

    Pass 1: scan taxonomy tokens longest-first, record positions of all matches.
    Pass 2: scan alias patterns; if the alias match is entirely within a region
            already claimed by a longer taxonomy match, skip it (prevents "js"
            from double-matching inside "next.js").
    """
    low = text.lower()
    found: list[str] = []
    seen: set[str] = set()

    # Pass 1 — direct taxonomy matches (longest first).
    claimed: list[tuple[int, int]] = []  # (start, end) of consumed spans
    for pattern, skill in _TAXONOMY_PATTERNS:
        for m in pattern.finditer(low):
            # Check not already claimed by a longer match
            s, e = m.start(), m.end()
            if not any(cs <= s and e <= ce for cs, ce in claimed):
                if skill not in seen:
                    found.append(skill)
                    seen.add(skill)
                claimed.append((s, e))

    # Pass 2 — alias matches (longest alias first), resolving to canonical.
    for pattern, canonical in _ALIAS_PATTERNS:
        if canonical in seen:
            continue  # already found via direct match
        for m in pattern.finditer(low):
            s, e = m.start(), m.end()
            # Skip if this span is inside a claimed taxonomy match (e.g. "js" in "next.js")
            if any(cs <= s and e <= ce for cs, ce in claimed):
                continue
            found.append(canonical)
            seen.add(canonical)
            claimed.append((s, e))
            break  # one match per alias is enough

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
