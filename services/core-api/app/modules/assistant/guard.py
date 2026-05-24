from __future__ import annotations

import re

_INJECTION_PATTERNS = (
    re.compile(r"(?i)ignore\s+(all\s+)?(previous|prior)\s+instructions"),
    re.compile(r"(?i)you\s+are\s+now\s+"),
    re.compile(r"(?i)system\s*:\s*"),
    re.compile(r"(?i)developer\s*:\s*"),
    re.compile(r"(?i)jailbreak"),
    re.compile(r"(?i)reveal\s+(the\s+)?(system\s+)?prompt"),
)


def looks_like_prompt_injection(message: str) -> bool:
    return any(pattern.search(message) for pattern in _INJECTION_PATTERNS)


def wrap_user_question(message: str) -> str:
    """Delimit untrusted user text for LLM prompts."""
    safe = message.replace("```", "").strip()
    return f"<<USER_QUESTION>>\n{safe}\n<</USER_QUESTION>>"


def llm_score_context(*, overall: float, bucket: str, jd_match: float, ats_safety: float) -> str:
    """Minimize identifiers sent to external LLM providers."""
    return (
        f"overall={round(overall)} bucket={bucket} "
        f"jd_match={round(jd_match)} ats_safety={round(ats_safety)}"
    )
