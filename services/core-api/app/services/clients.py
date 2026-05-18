import httpx

from ..config import AI_REWRITER_URL, ATS_ENGINE_URL


async def generate_resume_content(profile: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{AI_REWRITER_URL}/generate/resume", json=profile)
        resp.raise_for_status()
        return resp.json()


async def run_ats_scan(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{ATS_ENGINE_URL}/scan", json=payload)
        resp.raise_for_status()
        return resp.json()
