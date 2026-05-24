from __future__ import annotations

from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .models.entities import User
from .services.auth import get_user_by_token


def _extract_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or malformed Authorization header")
    return authorization.split(" ", 1)[1]


def current_user(
    authorization: Optional[str] = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    """Require any authenticated user."""
    token = _extract_token(authorization)
    user = get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


def require_student(user: User = Depends(current_user)) -> User:
    """Require role == student (or admin)."""
    if user.role not in ("student", "admin"):
        raise HTTPException(status_code=403, detail="Student access required")
    return user


def require_officer(user: User = Depends(current_user)) -> User:
    """Require role == officer (or admin)."""
    if user.role not in ("officer", "admin"):
        raise HTTPException(status_code=403, detail="Officer access required")
    return user


def require_admin(user: User = Depends(current_user)) -> User:
    """Require role == admin."""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user


# Handler / query-service factories — override via app.dependency_overrides in tests.
from .handler_dependencies import (  # noqa: E402
    get_agent_run_query_service,
    get_ats_query_service,
    get_ats_scan_handler,
    get_chat_handler,
    get_create_officer_batch_handler,
    get_dashboard_query_service,
    get_delete_resume_handler,
    get_export_query_service,
    get_generate_resume_handler,
    get_login_handler,
    get_logout_handler,
    get_officer_batch_query_service,
    get_officer_cohort_service,
    get_officer_dashboard_service,
    get_officer_heatmap_service,
    get_officer_readiness_report_service,
    get_officer_review_service,
    get_officer_skill_gaps_service,
    get_parse_jd_handler,
    get_profile_query_service,
    get_queue_export_handler,
    get_recommendation_query_service,
    get_register_handler,
    get_resume_query_service,
    get_run_agent_handler,
    get_run_rewrite_handler,
    get_score_resume_handler,
    get_upload_officer_batch_handler,
    get_upload_resume_handler,
    get_upsert_profile_handler,
)
