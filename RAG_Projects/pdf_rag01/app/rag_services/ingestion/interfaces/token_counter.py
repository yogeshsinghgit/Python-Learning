"""
Base interface for token counting implementations.
"""

from abc import ABC, abstractmethod

from app.rag_services.ingestion.tokenizers.models import TokenizationResult


class TokenCounter(ABC):
    """
    Tokenizes text and counts tokens.
    """

    @abstractmethod
    def tokenize(
        self,
        text: str,
    ) -> TokenizationResult:
        """
        Tokenize text and return token count + token ids.

        Args:
            text: Input text.

        Returns:
            TokenizationResult with token_count and token_ids.
        """
        raise NotImplementedError

    @abstractmethod
    def decode(
        self,
        token_ids: list[int],
    ) -> str:
        """
        Decode token ids back to text.

        Args:
            token_ids: List of token ids.

        Returns:
            Decoded string.
        """
        raise NotImplementedError