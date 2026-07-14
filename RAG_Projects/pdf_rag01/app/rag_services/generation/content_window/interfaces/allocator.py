from abc import ABC, abstractmethod

from app.domains.generation.models import TokenBudget


class BudgetAllocator(ABC):

    @abstractmethod
    async def allocate(
        self,
        max_context_tokens: int,
        reserved_response_tokens: int,
    ) -> TokenBudget:
        ...