from abc import ABC, abstractmethod

from app.domains.generation.models import TokenizedMessage


class HistoryTruncator(ABC):

    @abstractmethod
    async def truncate(
        self,
        history: list[TokenizedMessage],
        token_budget: int,
    ) -> list[TokenizedMessage]:
        ...