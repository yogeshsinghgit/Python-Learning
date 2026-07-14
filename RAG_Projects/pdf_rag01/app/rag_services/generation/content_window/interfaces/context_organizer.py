from abc import ABC, abstractmethod

from app.domains.generation.models import TokenizedContextChunk


class ContextOrganizer(ABC):

    @abstractmethod
    async def organize(
        self,
        chunks: list[TokenizedContextChunk],
    ) -> list[TokenizedContextChunk]:
        ...