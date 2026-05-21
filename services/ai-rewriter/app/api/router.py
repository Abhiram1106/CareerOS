from fastapi import APIRouter

from .controllers.rewrite_controller import router as rewrite_router

api_router = APIRouter()
api_router.include_router(rewrite_router, tags=["rewrite"])
