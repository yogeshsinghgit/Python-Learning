from abc import ABC, abstractmethod

from app.domains.generation.models import (
    GenerationResult,
    LLMResponse,
)


class ResponseParser(ABC):

    @abstractmethod
    async def parse(
        self,
        response: LLMResponse,
    ) -> GenerationResult:
        ...