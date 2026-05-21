from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.router import api_router
from .db_bootstrap import DatabaseNotReadyError, bootstrap_database

app = FastAPI(title="CareerOS Campus AI — Core API", version="0.4.0")
app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
def startup_db_guard():
    try:
        bootstrap_database()
    except DatabaseNotReadyError as exc:
        raise RuntimeError(str(exc)) from exc
