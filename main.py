from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
import uvicorn

from core import settings

from api import router as api_router

from core.models import db_helper
from core.models import client_manager


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manage the application lifecycle.

    :param app: FastAPI application instance
    :yield: None
    """
    # Startup
    await client_manager.start()
    yield
    # Shutdown
    await db_helper.dispose()
    await client_manager.dispose_all_clients()

    # TODO: Idea how to clean up expired tokens
    # async with db_helper.session_getter() as session:
    #     await cleanup_expired_tokens(session)


main_app = FastAPI(lifespan=lifespan)

main_app.include_router(api_router, prefix=settings.api.prefix, tags=["AI"])


if __name__ == "__main__":
    uvicorn.run("main:main_app", host=settings.run.host, port=settings.run.port,
                reload=settings.run.debug)
