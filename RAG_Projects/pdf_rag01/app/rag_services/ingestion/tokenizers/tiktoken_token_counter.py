"""
Tiktoken implementation of the TokenCounter interface.
"""

from __future__ import annotations

import tiktoken
from loguru import logger

from app.core.config import get_settings
from app.rag_services.ingestion.interfaces.token_counter import TokenCounter
from app.rag_services.ingestion.tokenizers.models import TokenizationResult


class TiktokenTokenCounter(TokenCounter):
    """
    Tokenizes text and counts tokens using OpenAI's tiktoken library.
    """

    def __init__(
        self,
        encoding_name: str | None = None,
    ) -> None:
        settings = get_settings()

        self._encoding_name = (
            encoding_name or settings.tokenizer_encoding
        )

        self._encoding = tiktoken.get_encoding(
            self._encoding_name,
        )

        logger.info(
            f"Initialized TiktokenTokenCounter "
            f"with encoding='{self._encoding_name}'."
        )

    def tokenize(
        self,
        text: str,
    ) -> TokenizationResult:
        """
        Tokenize text into token IDs and return count + ids.
        """

        if not text:
            return TokenizationResult(token_count=0)

        token_ids = self._encoding.encode(text)

        logger.debug(
            f"Generated {len(token_ids)} tokens."
        )

        return TokenizationResult(
            token_count=len(token_ids),
            token_ids=token_ids,
        )

    def decode(
        self,
        token_ids: list[int],
    ) -> str:
        """
        Decode token ids back to text.
        """
        return self._encoding.decode(token_ids)