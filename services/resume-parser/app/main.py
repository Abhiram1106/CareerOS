"""CareerOS Resume Parser — FastAPI service.

Accepts PDF or DOCX file bytes, returns structured section JSON
and ATS parse-safety flags.

Port: 8004 (internal only — called via core-api/clients.py)
"""
from __future__ import annotations

from fastapi import FastAPI

from .api.router import api_router

app = FastAPI(title="CareerOS Resume Parser", version="0.2.0")
app.include_router(api_router)


@app.get("/health")
def health():
    return {"status": "ok"}
