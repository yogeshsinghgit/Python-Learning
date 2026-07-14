import tiktoken

from loguru import logger


class TikTokenCounter(TokenCounter):

    def __init__(
        self,
        encoding_name: str = "cl100k_base",
    ) -> None:

        self._encoding = tiktoken.get_encoding(
            encoding_name
        )

    async def count(
        self,
        text: str,
    ) -> int:

        tokens = len(
            self._encoding.encode(text)
        )

        logger.debug(
            f"Token count: {tokens}"
        )

        return tokens

    async def count_messages(
        self,
        messages: list[str],
    ) -> int:

        total = 0

        for message in messages:
            total += await self.count(message)

        return total