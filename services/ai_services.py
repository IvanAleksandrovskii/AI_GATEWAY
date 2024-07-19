from typing import Optional
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from core.schemas import Response
from core.models import AIProvider


async def query_aimlapi(model: AIProvider, message: str) -> Optional[str]:
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                model.api_url,
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": message}]
                },
                headers={"Authorization": f"Bearer {model.api_key}"},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        except (httpx.RequestError, KeyError):
            return None


async def query_ai_model(model: AIProvider, message: str) -> Optional[str]:
    if model.name == "AIMLapi":
        return await query_aimlapi(model, message)
    return None


async def get_ai_response(db: AsyncSession, message: str) -> Response:
    models_query = select(AIProvider).order_by(AIProvider.priority)
    result = await db.execute(models_query)
    ai_models = result.scalars().all()

    for model in ai_models:
        response = await query_ai_model(model, message)
        if response:
            return Response(content=response, ai_model=model.name)

    return Response(content="No response from AI models.", ai_model="None")


async def get_ai_models(db: AsyncSession) -> list[str]:
    models_list = []

    models_query = select(AIProvider).order_by(AIProvider.priority)
    result = await db.execute(models_query)
    ai_models = result.scalars().all()

    for model in ai_models:
        models_list.append(model.name)

    return models_list
