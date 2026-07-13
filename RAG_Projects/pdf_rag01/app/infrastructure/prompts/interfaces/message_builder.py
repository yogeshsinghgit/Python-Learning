from abc import ABC, abstractmethod

from app.domains.generation.models import (
    ChatMessage,
    RenderedPrompt,
)


class MessageBuilder(ABC):

    @abstractmethod
    async def build(
        self,
        prompt: RenderedPrompt,
        history: list[ChatMessage],
    ) -> list[ChatMessage]:
        ...