from abc import ABC, abstractmethod

from app.domains.generation.models import (
    GenerationRequest,
    GenerationResult,
)


class GenerationPipeline(ABC):

    @abstractmethod
    async def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResult:
        ...