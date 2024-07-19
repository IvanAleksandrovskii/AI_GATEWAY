from typing import Optional, List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas import Response, Message

from services import get_ai_models, get_ai_response

router = APIRouter()


@router.post("/message/", response_model=Response)
async def process_message(
    message: Message,
    ai_model: Optional[str] = None,
    db: AsyncSession = Depends(db_helper.session_getter)
):
    return await get_ai_response(db, message.content, ai_model)


# TODO: view returns list of strings. Need to improve to json and rebuild for business logic
@router.get("/models/", response_model=List[str])
async def get_all_ai_models(db: AsyncSession = Depends(db_helper.session_getter)):
    return await get_ai_models(db)
