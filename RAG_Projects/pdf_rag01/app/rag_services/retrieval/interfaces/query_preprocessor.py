from abc import ABC, abstractmethod


class QueryPreprocessor(ABC):
    """
    Defines the contract for preprocessing a user query before
    embedding generation.

    Future implementations may perform:
    - Query normalization
    - Spell correction
    - Acronym expansion
    - Query rewriting
    - HyDE
    - Multi-query generation
    """

    @abstractmethod
    async def preprocess(self, query: str) -> str:
        """
        Preprocess the user query.

        Args:
            query: Raw user query.

        Returns:
            Normalized query.
        """
        raise NotImplementedError