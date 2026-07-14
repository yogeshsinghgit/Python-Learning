from abc import ABC, abstractmethod

from app.domains.generation.models import (
    TokenizedContextChunk,
)


class ContextTruncator(ABC):

    @abstractmethod
    async def truncate(
        self,
        chunks: list[TokenizedContextChunk],
        token_budget: int,
    ) -> list[TokenizedContextChunk]:
        ...