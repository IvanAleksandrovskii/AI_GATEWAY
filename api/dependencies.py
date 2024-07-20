from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from services import validate_token

security = HTTPBearer()


async def validate_token_header(
    token: str = Header(..., description="Access token"),
    db: AsyncSession = Depends(db_helper.session_getter)
):
    if not await validate_token(db, token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )
    return token
