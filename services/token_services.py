from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import cast, DateTime
from sqlalchemy import select, func, delete
from core.models.token import Token
import secrets
import string


def generate_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


async def create_token(db: AsyncSession, expiration_minutes=300):
    token = generate_token()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    db_token = Token(token=token, expires_at=expires_at)
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token


async def validate_token(db: AsyncSession, token: str):
    result = await db.execute(select(Token).where(Token.token == token))
    db_token = result.scalars().first()
    if db_token:
        if db_token.is_active is False:
            return False
        return db_token.is_active
    return False


async def get_latest_active_token(db: AsyncSession):
    result = await db.execute(
        select(Token)
        .where(Token.is_active == True)
        .where(Token.expires_at > cast(func.now(), DateTime(timezone=True)))
        .order_by(Token.created_at.desc())
        .limit(1)
    )
    return result.scalars().first()


async def create_new_token_if_needed(db: AsyncSession):
    latest_token = await get_latest_active_token(db)
    if not latest_token or not latest_token.is_active:
        return await create_token(db)
    return latest_token

# TODO: Idea how to clean up expired tokens
# async def cleanup_expired_tokens(db: AsyncSession):
#     current_time = datetime.now(timezone.utc)
#     await db.execute(delete(Token).where(Token.expires_at < current_time))
#     await db.commit()
