from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from core.schemas import Response, Message

from services import ai_services

router = APIRouter()


@router.post("/message", response_model=Response)
async def process_message(message: Message, db: AsyncSession = Depends(db_helper.session_getter)):
    return await ai_services.get_ai_response(db, message.content)
