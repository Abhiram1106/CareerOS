from __future__ import annotations

import re

_EMAIL = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
_PHONE = re.compile(r"\b\d{10}\b")


def redact_text(value: str, *, max_len: int = 500) -> str:
    """Strip common PII patterns before writing assistant or audit payloads to logs."""
    cleaned = _EMAIL.sub("[email]", value)
    cleaned = _PHONE.sub("[phone]", cleaned)
    if len(cleaned) > max_len:
        return cleaned[:max_len] + "…"
    return cleaned
