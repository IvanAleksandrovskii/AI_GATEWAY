from typing import Optional, List
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core import logger
from core.schemas import Response
from core.models import AIProvider
from core.models import client_manager


# TODO: Improve error handling
async def query_ai_provider(model: AIProvider, message: str) -> Optional[str]:
    """
    Send a query to the specified AI provider and return the response.

    :param model: AIProvider model containing API details
    :param message: User's input message
    :return: AI-generated response or None if request fails
    """
    retries = 2  # Number of retries
    uber_client = None

    for attempt in range(retries):
        try:
            uber_client = await client_manager.get_client()
            response = await uber_client.client.post(
                model.api_url,
                json=model.get_request_payload(message),
                headers=model.get_headers(),
                timeout=30.0
            )
            response.raise_for_status()
            return await model.parse_response(response.json())
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:
                logger.warning(f"Rate limit exceeded for %r!", model.name)
                return None
            logger.error(f"Failed to query %r!: %s", model.name, e)
        except (httpx.RequestError, KeyError) as e:
            logger.error(f"Error querying %r!: %s", model.name, e)
        finally:
            if uber_client:
                await client_manager.release_client(uber_client)

    return None


async def get_ai_response(db: AsyncSession, message: str, specific_model: Optional[str] = None) -> Response:
    """
    Get an AI response for the given message, optionally from a specific AI model.

    :param db: AsyncSession for database operations
    :param message: User's input message
    :param specific_model: Optional name of a specific AI model to use
    :return: Response object containing the AI-generated content
    """
    if specific_model:
        model = await db.execute(select(AIProvider).where(AIProvider.name == specific_model))
        model = model.scalar_one_or_none()
        if not model:
            return Response(content="Specified AI model not found.", ai_model="None", request_content=message)

        response = await query_ai_provider(model, message)
        if response:
            return Response(request_content=message, content=response, ai_model=model.name)
        return Response(content="No response from specified AI model.", ai_model="None", request_content=message)

    models_query = select(AIProvider).order_by(AIProvider.priority)
    result = await db.execute(models_query)
    ai_models = result.scalars().all()

    for model in ai_models:
        response = await query_ai_provider(model, message)
        if response:
            return Response(request_content=message, content=response, ai_model=model.name)

    return Response(content="No successful response from any AI models.", ai_model="None", request_content=message)


# TODO: view returns list of strings. Need to improve to json and rebuild for business logic
async def get_ai_models(db: AsyncSession) -> List[str]:
    """
    Get a list of AI model names from the database.

    :param db: AsyncSession for database operations
    :return: List of AI model names (AIProvider.name)
    """
    models_query = select(AIProvider).order_by(AIProvider.priority)
    result = await db.execute(models_query)
    ai_models = result.scalars().all()
    return [model.name for model in ai_models]
