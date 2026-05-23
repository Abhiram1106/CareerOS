from fastapi import APIRouter

from .controllers.parse_safety_controller import router as parse_safety_router

api_router = APIRouter()
api_router.include_router(parse_safety_router, tags=["ats"])
