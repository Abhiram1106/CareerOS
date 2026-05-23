from __future__ import annotations

import httpx
from fastapi import HTTPException

from ..config import AI_REWRITER_URL, ATS_ENGINE_URL, MATCH_ENGINE_URL, RESUME_PARSER_URL


async def generate_resume_content(profile: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{AI_REWRITER_URL}/generate/resume", json=profile)
        resp.raise_for_status()
        return resp.json()


async def run_ats_parse_safety(ats_flags: list[str]) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.post(
                f"{ATS_ENGINE_URL}/parse-safety",
                json={"ats_flags": ats_flags},
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="ATS engine unavailable") from exc


async def parse_resume_file(file_content: bytes, filename: str, content_type: str) -> dict:
    """Call resume-parser service with the raw file bytes."""
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(
                f"{RESUME_PARSER_URL}/parse",
                files={"file": (filename, file_content, content_type)},
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:300]
            raise HTTPException(status_code=exc.response.status_code, detail=f"Resume parser: {detail}") from exc
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="Resume parser service unavailable") from exc


async def parse_jd_text(jd_text: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.post(f"{MATCH_ENGINE_URL}/jd/parse", json={"jd_text": jd_text})
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="Match engine unavailable") from exc


async def match_resume_to_jd(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(f"{MATCH_ENGINE_URL}/match", json=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="Match engine unavailable") from exc
