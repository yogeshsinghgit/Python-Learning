from loguru import logger

from app.domains.generation.models import TokenizedMessage
from app.rag_services.generation.content_window.interfaces.history_truncator import (
    HistoryTruncator
)

class DefaultHistoryTruncator(HistoryTruncator):

    async def truncate(
        self,
        history: list[TokenizedMessage],
        token_budget: int,
    ) -> list[TokenizedMessage]:

        logger.debug(
            f"History budget: {token_budget}"
        )

        selected: list[TokenizedMessage] = []

        total_tokens = 0

        #
        # Keep newest messages first
        #

        for message in reversed(history):

            if (
                total_tokens + message.token_count
                > token_budget
            ):
                break

            selected.append(message)

            total_tokens += message.token_count

        selected.reverse()

        logger.info(
            f"Selected {len(selected)} history messages "
            f"({total_tokens} tokens)"
        )

        return selected