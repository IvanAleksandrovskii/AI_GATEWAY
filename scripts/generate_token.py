import asyncio

from core.models import db_helper
from services import create_new_token_if_needed


async def generate_token():
    async for session in db_helper.session_getter():
        token = await create_new_token_if_needed(session)
        print(f"Active token: {token.token}")
        print(f"Expires at: {token.expires_at}")

if __name__ == "__main__":
    asyncio.run(generate_token())
