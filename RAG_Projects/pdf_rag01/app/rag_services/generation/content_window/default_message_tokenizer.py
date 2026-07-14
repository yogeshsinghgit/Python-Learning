from loguru import logger

from app.domains.generation.models import (
    ChatMessage,
    ContextChunk,
    TokenizedContextChunk,
    TokenizedMessage,
)

from app.rag_services.generation.content_window.interfaces.message_tokenizer import MessageTokenizer
from app.rag_services.generation.content_window.interfaces.token_counter import TokenCounter


class DefaultMessageTokenizer(MessageTokenizer):

    def __init__(
        self,
        token_counter: TokenCounter,
    ) -> None:

        self._token_counter = token_counter

    async def tokenize_messages(
        self,
        messages: list[ChatMessage],
    ) -> list[TokenizedMessage]:

        tokenized: list[TokenizedMessage] = []

        for message in messages:

            tokens = await self._token_counter.count(
                message.content
            )

            tokenized.append(
                TokenizedMessage(
                    message=message,
                    token_count=tokens,
                )
            )

        logger.debug(
            f"Tokenized {len(messages)} messages."
        )

        return tokenized

    async def tokenize_chunks(
        self,
        chunks: list[ContextChunk],
    ) -> list[TokenizedContextChunk]:

        tokenized: list[TokenizedContextChunk] = []

        for chunk in chunks:

            tokens = await self._token_counter.count(
                chunk.content
            )

            tokenized.append(
                TokenizedContextChunk(
                    chunk=chunk,
                    token_count=tokens,
                )
            )

        logger.debug(
            f"Tokenized {len(chunks)} context chunks."
        )

        return tokenized