from abc import ABC, abstractmethod

from app.domains.generation.models import (
    LLMRequest,
    LLMResponse,
)


class LLMClient(ABC):

    @abstractmethod
    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        ...