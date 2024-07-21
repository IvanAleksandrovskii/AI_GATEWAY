__all__ = ["router", "validate_token_header"]

from fastapi import APIRouter
from .ai_views import router as ai_router
from .dependencies import validate_token_header

router = APIRouter()

router.include_router(ai_router)
