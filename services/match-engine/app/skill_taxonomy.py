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


# ── CARE-RAG Layer 3D: Skill Graph Index ──────────────────────────────────────
#
# Directed adjacency graph: skill → list of (neighbour, distance) pairs.
# Distance semantics:
#   1 = direct prerequisite or common co-occurrence ("React needs JavaScript")
#   2 = same technology family ("React and Angular are both Frontend")
#   3 = same broad domain ("React dev likely also does REST API integration")
#
# Asymmetric edges reflect learning direction:
#   "You know Python" → suggest Pandas (d=1), SQL (d=1), Data Analyst role (d=2)
#   "You know Docker" → suggest Kubernetes (d=1), CI/CD (d=1), AWS (d=2)

SKILL_GRAPH: dict[str, list[tuple[str, int]]] = {
    # ── Python ecosystem ──────────────────────────────────────────────────────
    "python": [
        ("django", 1), ("fastapi", 1), ("flask", 1),
        ("pandas", 1), ("numpy", 1), ("scikit-learn", 1),
        ("sql", 1), ("rest api", 1),
        ("machine learning", 2), ("data structures", 2),
        ("algorithms", 2), ("postgresql", 2),
    ],
    "django": [("python", 1), ("postgresql", 1), ("rest api", 1), ("sql", 2)],
    "fastapi": [("python", 1), ("rest api", 1), ("postgresql", 2), ("docker", 2)],
    "flask": [("python", 1), ("rest api", 1), ("sql", 2)],

    # ── Data / ML ecosystem ───────────────────────────────────────────────────
    "pandas": [("python", 1), ("numpy", 1), ("sql", 1), ("scikit-learn", 2), ("tableau", 2)],
    "numpy": [("python", 1), ("pandas", 1), ("scikit-learn", 2)],
    "scikit-learn": [("python", 1), ("pandas", 1), ("machine learning", 1), ("numpy", 2)],
    "tensorflow": [("python", 1), ("keras", 1), ("deep learning", 1), ("machine learning", 2)],
    "pytorch": [("python", 1), ("deep learning", 1), ("machine learning", 2), ("keras", 2)],
    "keras": [("tensorflow", 1), ("pytorch", 1), ("deep learning", 1), ("python", 2)],
    "machine learning": [("python", 1), ("scikit-learn", 1), ("pandas", 1), ("sql", 2)],
    "deep learning": [("tensorflow", 1), ("pytorch", 1), ("python", 2), ("machine learning", 2)],
    "tableau": [("sql", 1), ("pandas", 2), ("excel", 2), ("power bi", 2)],
    "power bi": [("sql", 1), ("excel", 1), ("tableau", 2)],
    "excel": [("sql", 1), ("power bi", 2), ("tableau", 2)],

    # ── JavaScript ecosystem ──────────────────────────────────────────────────
    "javascript": [
        ("typescript", 1), ("react", 1), ("node.js", 1),
        ("html", 1), ("css", 1), ("rest api", 2),
    ],
    "typescript": [("javascript", 1), ("react", 1), ("node.js", 1), ("angular", 2)],
    "react": [("javascript", 1), ("typescript", 1), ("rest api", 1), ("node.js", 2)],
    "react.js": [("javascript", 1), ("typescript", 1), ("rest api", 1)],
    "angular": [("typescript", 1), ("javascript", 2), ("rest api", 2)],
    "vue": [("javascript", 1), ("typescript", 2), ("rest api", 2)],
    "next.js": [("react", 1), ("javascript", 1), ("typescript", 2)],
    "node.js": [("javascript", 1), ("express", 1), ("rest api", 1), ("typescript", 2)],
    "express": [("node.js", 1), ("javascript", 1), ("rest api", 1), ("mongodb", 2)],
    "html": [("css", 1), ("javascript", 1), ("react", 2)],
    "css": [("html", 1), ("javascript", 1), ("react", 2)],
    "graphql": [("rest api", 1), ("javascript", 2), ("node.js", 2)],

    # ── Java ecosystem ────────────────────────────────────────────────────────
    "java": [
        ("spring boot", 1), ("spring", 1), ("sql", 1),
        ("object oriented programming", 1), ("oop", 1),
        ("algorithms", 2), ("data structures", 2),
    ],
    "spring boot": [("java", 1), ("spring", 1), ("sql", 1), ("rest api", 1), ("docker", 2)],
    "spring": [("java", 1), ("spring boot", 1), ("sql", 2)],
    "kotlin": [("java", 1), ("spring boot", 2), ("android", 2)],

    # ── DevOps / Cloud ecosystem ──────────────────────────────────────────────
    "docker": [
        ("kubernetes", 1), ("ci/cd", 1), ("linux", 1),
        ("aws", 2), ("gcp", 2), ("azure", 2),
    ],
    "kubernetes": [("docker", 1), ("ci/cd", 1), ("aws", 2), ("terraform", 2)],
    "aws": [("docker", 1), ("kubernetes", 2), ("terraform", 1), ("ci/cd", 2)],
    "gcp": [("docker", 1), ("terraform", 1), ("kubernetes", 2)],
    "azure": [("docker", 1), ("terraform", 1), ("kubernetes", 2)],
    "terraform": [("aws", 1), ("gcp", 1), ("azure", 1), ("docker", 2)],
    "ci/cd": [("docker", 1), ("jenkins", 1), ("github", 1), ("kubernetes", 2)],
    "jenkins": [("ci/cd", 1), ("docker", 2), ("git", 2)],
    "linux": [("bash", 1), ("docker", 2), ("git", 2)],
    "bash": [("linux", 1), ("shell scripting", 1), ("git", 2)],
    "shell scripting": [("bash", 1), ("linux", 1)],

    # ── Databases ─────────────────────────────────────────────────────────────
    "sql": [
        ("postgresql", 1), ("mysql", 1), ("python", 2),
        ("pandas", 2), ("tableau", 2), ("data structures", 3),
    ],
    "postgresql": [("sql", 1), ("python", 2), ("docker", 2)],
    "mysql": [("sql", 1), ("php", 2)],
    "mongodb": [("node.js", 1), ("express", 1), ("nosql", 2)],
    "redis": [("docker", 2), ("python", 2), ("node.js", 2)],
    "elasticsearch": [("kibana", 1), ("python", 2), ("docker", 2)],
    "kafka": [("docker", 2), ("python", 2), ("java", 2)],

    # ── Version control / collaboration ──────────────────────────────────────
    "git": [("github", 1), ("gitlab", 1), ("ci/cd", 2)],
    "github": [("git", 1), ("ci/cd", 1), ("gitlab", 2)],
    "gitlab": [("git", 1), ("ci/cd", 1), ("github", 2)],

    # ── Core CS concepts ──────────────────────────────────────────────────────
    "data structures": [("algorithms", 1), ("python", 2), ("java", 2)],
    "algorithms": [("data structures", 1), ("python", 2), ("java", 2)],
    "object oriented programming": [("java", 1), ("python", 1), ("c++", 2), ("oop", 1)],
    "oop": [("object oriented programming", 1), ("java", 1), ("python", 1)],
    "system design": [("microservices", 1), ("docker", 2), ("rest api", 2)],
    "microservices": [("docker", 1), ("kubernetes", 1), ("rest api", 1), ("system design", 2)],
    "rest api": [("python", 2), ("javascript", 2), ("fastapi", 2), ("spring boot", 2)],

    # ── Other ─────────────────────────────────────────────────────────────────
    "agile": [("scrum", 1), ("jira", 1)],
    "scrum": [("agile", 1), ("jira", 1)],
    "jira": [("agile", 1), ("scrum", 1)],
    "golang": [("docker", 2), ("kubernetes", 2), ("microservices", 2)],
    "rust": [("golang", 2), ("c++", 2), ("algorithms", 2)],
    "c++": [("algorithms", 1), ("data structures", 1), ("rust", 2), ("golang", 2)],
    "c#": [(".net", 1), ("azure", 2), ("java", 2)],
    ".net": [("c#", 1), ("azure", 2)],
    "swift": [("ios", 1), ("kotlin", 2)],
    "kotlin": [("java", 1), ("android", 2), ("swift", 2)],
}


def get_adjacent_skills(
    known_skills: list[str],
    max_distance: int = 1,
    exclude: set[str] | None = None,
    limit: int = 10,
) -> list[tuple[str, int]]:
    """Return skills adjacent to the known set, ordered by minimum distance.

    Args:
        known_skills: Skills the candidate already has.
        max_distance: Maximum hop distance to consider (1=direct, 2=same family).
        exclude: Skills already in resume or already suggested — skip these.
        limit: Max results to return.

    Returns:
        List of (skill, min_distance) sorted by distance then alphabetically.
    """
    known = {s.lower() for s in known_skills}
    blocked = (exclude or set()) | known
    found: dict[str, int] = {}  # skill → best (minimum) distance seen

    for skill in known:
        neighbours = SKILL_GRAPH.get(skill, [])
        for neighbour, dist in neighbours:
            if dist > max_distance:
                continue
            if neighbour in blocked:
                continue
            if neighbour not in found or dist < found[neighbour]:
                found[neighbour] = dist

    results = sorted(found.items(), key=lambda x: (x[1], x[0]))
    return results[:limit]


def skill_gap_with_graph(
    known_skills: list[str],
    missing_jd_skills: list[str],
) -> list[dict]:
    """Enrich missing JD skills with graph-based adjacency context.

    For each missing skill, compute the minimum hop distance from the
    candidate's known skills. This distinguishes:
      - "You don't have Docker" (you know Linux — it's 2 hops away)
      - "You don't have Rust" (none of your skills are close)

    Returns enriched dicts: {skill, distance, nearest_known, reachable}.
    """
    known = {s.lower() for s in known_skills}
    results: list[dict] = []

    for missing in missing_jd_skills:
        m = missing.lower()
        best_dist: int | None = None
        nearest: str | None = None

        # Check if any known skill can reach this missing skill
        for known_skill in known:
            neighbours = SKILL_GRAPH.get(known_skill, [])
            for neighbour, dist in neighbours:
                if neighbour == m:
                    if best_dist is None or dist < best_dist:
                        best_dist = dist
                        nearest = known_skill

        results.append({
            "skill": missing,
            "distance": best_dist,            # None = no path in graph
            "nearest_known": nearest,          # which of your skills is closest
            "reachable": best_dist is not None,
        })

    # Sort: reachable skills first (easier to add), then by distance, then alpha
    results.sort(key=lambda x: (not x["reachable"], x["distance"] or 99, x["skill"]))
    return results
