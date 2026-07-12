from abc import ABC, abstractmethod

from app.rag_services.retrieval.models.llm_context import LLMContext
from app.rag_services.retrieval.models.retrieval_result import RetrievalResult


class ContextBuilder(ABC):
    """
    Builds an LLM-ready context from retrieval results.
    """

    @abstractmethod
    async def build(
        self,
        results: list[RetrievalResult],
    ) -> LLMContext:
        """
        Build an LLM context.

        Args:
            results:
                Ranked retrieval results.

        Returns:
            LLMContext
        """
        raise NotImplementedError