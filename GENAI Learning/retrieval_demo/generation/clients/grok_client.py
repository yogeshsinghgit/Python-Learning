from openai import AsyncOpenAI
from loguru import logger

from generation.clients.llm_client import LLMClient
from generation.models.prompt import PromptModel
from generation.models.result import LLMResult


class GrokClient(LLMClient):

    def __init__(
        self,
        api_key: str,
        model: LLMResult,
    ) -> None:

        self._model = model

        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1",
        )

    async def generate(
        self,
        prompt: PromptModel,
    ) -> str:

        logger.info(
            f"Generating response using model {self._model}"
        )

        try:

            response = await self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": prompt.system_prompt,
                    },
                    {
                        "role": "user",
                        "content": prompt.user_prompt,
                    },
                ],
                temperature=0,
            )

            # return response.choices[0].message.content
            usage = response.usage

            return LLMResult(
                answer=response.choices[0].message.content,
                model=response.model,
                input_tokens=usage.prompt_tokens,
                output_tokens=usage.completion_tokens,
                total_tokens=usage.total_tokens,
                finish_reason=response.choices[0].finish_reason,
            )

        except Exception as exc:

            logger.exception(
                f"Grok request failed: {exc}"
            )

            raise