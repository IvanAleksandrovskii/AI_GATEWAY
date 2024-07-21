from fastapi import APIRouter
from .ai_views import router as ai_router

router = APIRouter()

router.include_router(ai_router)
