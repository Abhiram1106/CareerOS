from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import text

from .api.router import api_router
from .database import SessionLocal
from .db_bootstrap import DatabaseNotReadyError, bootstrap_database
from .middleware.rate_limit import RateLimitMiddleware
from .middleware.security_headers import SecurityHeadersMiddleware

app = FastAPI(title="CareerOS Student AI — Core API", version="0.5.0")
app.include_router(api_router)
app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware)
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


@app.get("/ready")
def ready():
    """K8s-style readiness — verifies database connectivity."""
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "ok"}
    except Exception as exc:
        return {"status": "not_ready", "database": str(exc)}
    finally:
        db.close()


@app.on_event("startup")
def startup_db_guard():
    try:
        bootstrap_database()
    except DatabaseNotReadyError as exc:
        raise RuntimeError(str(exc)) from exc
