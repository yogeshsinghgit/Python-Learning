from __future__ import annotations

from openai import AsyncOpenAI
from loguru import logger

from app.core.config import settings
from app.infrastructure.llm.interfaces.client import LLMClient
from app.infrastructure.llm.models import (
    LLMRequest,
    LLMResponse,
)


class GrokClient(LLMClient):

    def __init__(self) -> None:

        self._client = AsyncOpenAI(
            api_key=settings.grok_api_key,
            base_url=settings.grok_base_url,
        )

        self._model = settings.grok_model

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        logger.info(
            f"Generating response using model '{self._model}'."
        )

        try:

            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": message.role.value,
                        "content": message.content,
                    }
                    for message in request.messages
                ],
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                stream=request.stream,
            )

            choice = response.choices[0]

            usage = response.usage

            logger.success(
                "LLM response generated successfully."
            )

            return LLMResponse(
                content=choice.message.content or "",
                finish_reason=choice.finish_reason,
                prompt_tokens=usage.prompt_tokens if usage else 0,
                completion_tokens=usage.completion_tokens if usage else 0,
                total_tokens=usage.total_tokens if usage else 0,
                raw_response=response.model_dump(),
            )

        except Exception as exc:

            logger.exception(
                f"Failed to generate response: {exc}"
            )

            raise