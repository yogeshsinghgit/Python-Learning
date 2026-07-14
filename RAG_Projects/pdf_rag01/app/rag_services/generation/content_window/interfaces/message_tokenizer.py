from abc import ABC, abstractmethod

from app.domains.generation.models import (
    ChatMessage,
    ContextChunk,
    TokenizedContextChunk,
    TokenizedMessage,
)


class MessageTokenizer(ABC):

    @abstractmethod
    async def tokenize_messages(
        self,
        messages: list[ChatMessage],
    ) -> list[TokenizedMessage]:
        ...

    @abstractmethod
    async def tokenize_chunks(
        self,
        chunks: list[ContextChunk],
    ) -> list[TokenizedContextChunk]:
        ...