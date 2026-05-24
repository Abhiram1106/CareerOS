from __future__ import annotations

import httpx
from fastapi import HTTPException

from ....config import LLM_API_BASE, LLM_API_KEY, LLM_MODEL


async def complete_chat(*, system: str, user: str) -> str:
    if not LLM_API_KEY:
        raise HTTPException(status_code=503, detail="LLM not configured on server")
    url = f"{LLM_API_BASE.rstrip('/')}/chat/completions"
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.2,
        "max_tokens": 600,
    }
    headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail="LLM provider error") from exc
    data = resp.json()
    choices = data.get("choices") or []
    if not choices:
        raise HTTPException(status_code=502, detail="Empty LLM response")
    content = choices[0].get("message", {}).get("content")
    if not isinstance(content, str) or not content.strip():
        raise HTTPException(status_code=502, detail="Invalid LLM response")
    return content.strip()
