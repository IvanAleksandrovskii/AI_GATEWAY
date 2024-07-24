from typing import Optional, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.dependencies import validate_token_header
from core.models import db_helper
from core.schemas import Response, Message

from services import get_ai_models, get_ai_response

router = APIRouter()


@router.post("/message/", response_model=Response)
async def process_message(
    message: Message,
    ai_model: Optional[str] = None,
    db: AsyncSession = Depends(db_helper.session_getter),
    token: str = Depends(validate_token_header)
):
    """Process a message and return an AI-generated response."""
    try:
        return await get_ai_response(db, message.content, ai_model)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


# TODO: Need to improve for business logic
@router.get("/models/", response_model=List[str])
async def get_all_ai_models(
    db: AsyncSession = Depends(db_helper.session_getter),
    token: str = Depends(validate_token_header)
):
    """List all available AI models."""
    try:
        return await get_ai_models(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
