from loguru import logger

from app.domains.generation.models import (
    GenerationResult,
    LLMResponse,
)

from app.rag_services.generation.content_window.interfaces.response_parser import (
    ResponseParser
)

class DefaultResponseParser(ResponseParser):

    async def parse(
        self,
        response: LLMResponse,
    ) -> GenerationResult:

        logger.debug("Parsing LLM response.")

        return GenerationResult(
            answer=response.content,
            usage=response.usage,
            raw_response=response.content,
        )