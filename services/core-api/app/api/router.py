"""Aggregate API routers. Domain controllers mount here as they are migrated."""

from fastapi import APIRouter

from .controllers.ats_controller import router as ats_router
from .controllers.auth_controller import router as auth_router
from .controllers.dashboard_controller import router as dashboard_router
from .controllers.export_controller import router as export_router
from .controllers.profile_controller import router as profile_router
from .controllers.resume_controller import router as resume_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(profile_router, tags=["profile"])
api_router.include_router(resume_router, tags=["resume"])
api_router.include_router(export_router, tags=["export"])
api_router.include_router(ats_router, tags=["ats"])
api_router.include_router(dashboard_router, tags=["dashboard"])
