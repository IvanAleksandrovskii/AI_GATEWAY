from typing import Optional, List
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.schemas import Response
from core.models import AIProvider


async def query_ai_provider(model: AIProvider, message: str) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                model.api_url,
                json=model.get_request_payload(message),
                headers=model.get_headers(),
                timeout=30.0
            )
            response.raise_for_status()
            return model.parse_response(response.json())
        except (httpx.RequestError, KeyError):
            return None


async def get_ai_response(db: AsyncSession, message: str, specific_model: Optional[str] = None) -> Response:
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

    return Response(content="No response from AI models.", ai_model="None", request_content=message)


# TODO: view returns list of strings. Need to improve to json and rebuild for business logic
async def get_ai_models(db: AsyncSession) -> List[str]:
    models_query = select(AIProvider).order_by(AIProvider.priority)
    result = await db.execute(models_query)
    ai_models = result.scalars().all()
    return [model.name for model in ai_models]
