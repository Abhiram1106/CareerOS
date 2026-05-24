"""Test bootstrap for core-api.

Sets up an in-memory SQLite DB shared across all sessions in a test run, forces
``AUTO_CREATE_TABLES=true`` so external HTTP services (resume-parser,
match-engine, ats-engine) are never contacted during unit tests, and overrides
the FastAPI ``get_db`` dependency to use the in-memory engine.

External clients (``parse_jd_text``, ``match_resume_to_jd``,
``ats_parse_safety``) are monkey-patched per-test to keep tests hermetic.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Force test-friendly config BEFORE importing app modules.
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("AUTO_CREATE_TABLES", "true")
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("RATE_LIMIT_ENABLED", "false")
os.environ.setdefault("LLM_API_KEY", "")
os.environ.setdefault("ENABLE_OFFICER_SURFACE", "true")

_CORE_API_ROOT = Path(__file__).resolve().parents[1]
if str(_CORE_API_ROOT) not in sys.path:
    sys.path.insert(0, str(_CORE_API_ROOT))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app


@pytest.fixture()
def engine():
    """Fresh in-memory SQLite engine per test (cheap with StaticPool)."""
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=eng)
    try:
        yield eng
    finally:
        eng.dispose()


@pytest.fixture()
def db_session(engine):
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(engine):
    """TestClient with get_db overridden to share the in-memory engine."""
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def _override_get_db():
        db = Session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
