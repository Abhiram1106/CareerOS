"""Aggregate API routers. Domain controllers mount here as they are migrated."""

from fastapi import APIRouter

from ..config import ENABLE_OFFICER_SURFACE
from .controllers.ats_controller import router as ats_router
from .controllers.auth_controller import router as auth_router
from .controllers.agent_controller import router as agent_router
from .controllers.dashboard_controller import router as dashboard_router
from .controllers.jd_controller import router as jd_router
from .controllers.jobs_controller import router as jobs_router
from .controllers.scorecard_controller import router as scorecard_router
from .controllers.recommendation_controller import router as recommendation_router
from .controllers.export_controller import router as export_router
from .controllers.profile_controller import router as profile_router
from .controllers.resume_controller import router as resume_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(agent_router, tags=["agent"])
api_router.include_router(profile_router, tags=["profile"])
api_router.include_router(resume_router, tags=["resume"])
api_router.include_router(export_router, tags=["export"])
api_router.include_router(ats_router, tags=["ats"])
if ENABLE_OFFICER_SURFACE:
    api_router.include_router(dashboard_router, tags=["dashboard"])
api_router.include_router(jd_router, tags=["jd"])
api_router.include_router(jobs_router, tags=["jobs"])
api_router.include_router(scorecard_router, tags=["scorecards"])
api_router.include_router(recommendation_router, tags=["recommendations"])
