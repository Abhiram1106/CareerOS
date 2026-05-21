from fastapi import APIRouter

from .controllers.parse_controller import router as parse_router

api_router = APIRouter()
api_router.include_router(parse_router, tags=["parse"])
