from typing import Optional

import httpx
from fastapi import HTTPException

from ..config import AI_INFERENCE_URL, ATS_ENGINE_URL, JOB_INTEL_URL, NEXUS_ATS_URL


async def generate_resume_content(profile: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{AI_INFERENCE_URL}/generate/resume", json=profile)
        resp.raise_for_status()
        return resp.json()


async def run_ats_scan(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{ATS_ENGINE_URL}/scan", json=payload)
        resp.raise_for_status()
        return resp.json()


async def get_job_matches(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{JOB_INTEL_URL}/matches", json=payload)
        resp.raise_for_status()
        return resp.json()


async def nexus_post(path: str, payload: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            resp = await client.post(f"{NEXUS_ATS_URL}{path}", json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"NEXUS ATS unavailable: {exc}") from exc


async def nexus_get(path: str, params: Optional[dict] = None) -> dict:
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            resp = await client.get(f"{NEXUS_ATS_URL}{path}", params=params)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"NEXUS ATS unavailable: {exc}") from exc


async def nexus_put(path: str, payload: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            resp = await client.put(f"{NEXUS_ATS_URL}{path}", json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"NEXUS ATS unavailable: {exc}") from exc


async def nexus_patch(path: str, payload: dict) -> dict:
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            resp = await client.patch(f"{NEXUS_ATS_URL}{path}", json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"NEXUS ATS unavailable: {exc}") from exc


async def nexus_delete(path: str) -> dict:
    try:
        async with httpx.AsyncClient(timeout=25) as client:
            resp = await client.delete(f"{NEXUS_ATS_URL}{path}")
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=502, detail=f"NEXUS ATS unavailable: {exc}") from exc
