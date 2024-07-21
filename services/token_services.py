import string
import secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import cast, DateTime
from sqlalchemy import select, func   # , delete

from core import settings
from core.models import Token


def generate_token(length=32):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


async def create_token(db: AsyncSession, expiration_minutes=settings.token.expiration_minutes):
    # expiration_days=settings.token.expiration_days
    """
    Create a new token with specified expiration time.

    :param db: AsyncSession for database operations
    :param expiration_minutes: Token validity period in minutes
    :return: New Token object
    """
    token = generate_token()
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiration_minutes)
    db_token = Token(token=token, expires_at=expires_at)
    db.add(db_token)
    await db.commit()
    await db.refresh(db_token)
    return db_token


async def validate_token(db: AsyncSession, token: str):
    """
    Validate the given token.

    :param db: AsyncSession for database operations
    :param token: Token string to validate
    :return: Boolean indicating if the token is valid and active
    """
    result = await db.execute(select(Token).where(Token.token == token))
    db_token = result.scalars().first()
    if db_token:
        if db_token.is_active is False:
            return False
        return db_token.is_active
    return False


async def get_latest_active_token(db: AsyncSession):
    """
    Get the latest active token from the database.

    :param db: AsyncSession for database operations
    :return: Token object or None if no token is found
    """
    result = await db.execute(
        select(Token)
        .where(Token.is_active == True)
        # TODO: is_active == True makes exactly the same as
        #  (Token.expires_at > cast(func.now(), DateTime(timezone=True))) (the one down below)
        #   keeping it for double checking purposes, mb remove it in the future
        .where(Token.expires_at > cast(func.now(), DateTime(timezone=True)))
        .order_by(Token.created_at.desc())
        .limit(1)
    )
    return result.scalars().first()


async def create_new_token_if_needed(db: AsyncSession):
    """
    Create a new token if no token is found an active one in the database.

    :param db: AsyncSession for database operations
    :return: Token object
    """
    latest_token = await get_latest_active_token(db)
    if not latest_token or not latest_token.is_active:
        return await create_token(db)
    return latest_token

# TODO: Idea how to clean up expired tokens
# async def cleanup_expired_tokens(db: AsyncSession):
#     current_time = datetime.now(timezone.utc)
#     await db.execute(delete(Token).where(Token.is_active == False))
#     await db.commit()
