from fastapi import APIRouter

from .controllers.scan_controller import router as scan_router

api_router = APIRouter()
api_router.include_router(scan_router, tags=["ats"])
