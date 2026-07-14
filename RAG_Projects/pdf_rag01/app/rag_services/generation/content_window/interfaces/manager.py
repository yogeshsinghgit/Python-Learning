from abc import ABC, abstractmethod

from app.domains.generation.models import (
    ChatMessage,
    ContextWindow,
    RetrievalContext,
)


class ContextWindowManager(ABC):

    @abstractmethod
    async def build(
        self,
        history: list[ChatMessage],
        retrieval_context: RetrievalContext,
        max_context_tokens: int,
        reserved_response_tokens: int,
    ) -> ContextWindow:
        ...