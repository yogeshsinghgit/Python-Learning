from abc import ABC, abstractmethod


class TokenCounter(ABC):

    @abstractmethod
    async def count(
        self,
        text: str,
    ) -> int:
        ...

    @abstractmethod
    async def count_messages(
        self,
        messages: list[str],
    ) -> int:
        ...