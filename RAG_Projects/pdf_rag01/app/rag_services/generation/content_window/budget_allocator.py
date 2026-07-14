from loguru import logger

from app.domains.generation.models import TokenBudget
from app.rag_services.generation.content_window.interfaces.allocator import BudgetAllocator


class DefaultBudgetAllocator(BudgetAllocator):

    async def allocate(
        self,
        max_context_tokens: int,
        reserved_response_tokens: int,
    ) -> TokenBudget:

        available = (
            max_context_tokens
            - reserved_response_tokens
        )

        budget = TokenBudget(
            max_context_tokens=max_context_tokens,
            reserved_response_tokens=reserved_response_tokens,
            system_budget=int(available * 0.10),
            history_budget=int(available * 0.20),
            context_budget=int(available * 0.60),
            query_budget=int(available * 0.10),
            available_budget=available,
        )

        logger.debug(
            f"Allocated token budget: {budget.model_dump()}"
        )

        return budget