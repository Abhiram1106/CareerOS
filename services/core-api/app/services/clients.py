from __future__ import annotations

import httpx
from fastapi import HTTPException

from ..config import (
    AI_REWRITER_URL,
    ATS_ENGINE_URL,
    JOBS_FEED_URL,
    MATCH_ENGINE_URL,
    RESUME_PARSER_URL,
)


async def generate_resume_content(profile: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{AI_REWRITER_URL}/generate/resume", json=profile)
        resp.raise_for_status()
        return resp.json()


async def generate_resume_from_profile(template_name: str, profile_data: dict) -> dict:
    """Generate resume from structured profile data using the chosen template."""
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.post(
                f"{AI_REWRITER_URL}/generate/from-profile",
                json={"template_name": template_name, "profile_data": profile_data},
            )
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="AI rewriter unavailable") from exc


async def proof_linked_rewrite(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30) as client:
        try:
            resp = await client.post(f"{AI_REWRITER_URL}/rewrite", json=payload)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="AI rewriter unavailable") from exc


async def run_ats_parse_safety(ats_flags: list[str], resume_text: str = "") -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.post(
                f"{ATS_ENGINE_URL}/parse-safety",
                json={"ats_flags": ats_flags, "resume_text": resume_text},
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


async def jobs_feed_search(query: str, location: str, page: int = 1) -> dict:
    params = {"q": query, "loc": location, "page": page}
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.get(f"{JOBS_FEED_URL}/jobs/search", params=params)
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="Jobs feed unavailable") from exc


async def jobs_feed_get(external_id: str) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            resp = await client.get(f"{JOBS_FEED_URL}/jobs/{external_id}")
            resp.raise_for_status()
            return resp.json()
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail="Jobs feed unavailable") from exc
