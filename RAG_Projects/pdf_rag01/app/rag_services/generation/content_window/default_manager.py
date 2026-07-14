from loguru import logger

from app.domains.generation.models import (
    ChatMessage,
    ContextWindow,
    RetrievalContext,
    TokenUsage,
)

from app.rag_services.generation.content_window.interfaces.allocator import (
    BudgetAllocator,
)
from app.rag_services.generation.content_window.interfaces.context_organizer import (
    ContextOrganizer,
)
from app.rag_services.generation.content_window.interfaces.context_truncator import (
    ContextTruncator,
)
from app.rag_services.generation.content_window.interfaces.history_truncator import (
    HistoryTruncator,
)
from app.rag_services.generation.content_window.interfaces.message_tokenizer import (
    MessageTokenizer,
)
from app.rag_services.generation.content_window.interfaces.manager import (
    ContextWindowManager,
)
from app.rag_services.generation.content_window.interfaces.token_counter import (
    TokenCounter,
)


class DefaultContextWindowManager(ContextWindowManager):

    def __init__(
        self,
        tokenizer: MessageTokenizer,
        allocator: BudgetAllocator,
        history_truncator: HistoryTruncator,
        context_truncator: ContextTruncator,
        context_organizer: ContextOrganizer,
        token_counter: TokenCounter,
    ) -> None:
        self._tokenizer = tokenizer
        self._allocator = allocator
        self._history_truncator = history_truncator
        self._context_truncator = context_truncator
        self._context_organizer = context_organizer
        self._token_counter = token_counter

    async def build(
        self,
        history: list[ChatMessage],
        retrieval_context: RetrievalContext,
        max_context_tokens: int,
        reserved_response_tokens: int,
    ) -> ContextWindow:

        logger.info("Building context window.")

        # ---------------------------------------------------------
        # Step 1 - Allocate token budgets
        # ---------------------------------------------------------

        budget = await self._allocator.allocate(
            max_context_tokens=max_context_tokens,
            reserved_response_tokens=reserved_response_tokens,
        )

        # ---------------------------------------------------------
        # Step 2 - Tokenize conversation history
        # ---------------------------------------------------------

        tokenized_history = await self._tokenizer.tokenize_messages(
            history
        )

        # ---------------------------------------------------------
        # Step 3 - Tokenize retrieved chunks
        # ---------------------------------------------------------

        tokenized_chunks = await self._tokenizer.tokenize_chunks(
            retrieval_context.results
        )

        # ---------------------------------------------------------
        # Step 4 - Truncate conversation history
        # ---------------------------------------------------------

        tokenized_history = await self._history_truncator.truncate(
            history=tokenized_history,
            token_budget=budget.history_budget,
        )

        # ---------------------------------------------------------
        # Step 5 - Truncate retrieved chunks
        # ---------------------------------------------------------

        tokenized_chunks = await self._context_truncator.truncate(
            chunks=tokenized_chunks,
            token_budget=budget.context_budget,
        )

        # ---------------------------------------------------------
        # Step 6 - Organize retrieved chunks
        # ---------------------------------------------------------

        tokenized_chunks = await self._context_organizer.organize(
            tokenized_chunks
        )

        # ---------------------------------------------------------
        # Step 7 - Build final context string
        # ---------------------------------------------------------

        context = "\n\n".join(
            chunk.chunk.content
            for chunk in tokenized_chunks
        )

        # ---------------------------------------------------------
        # Step 8 - Calculate token usage
        # ---------------------------------------------------------

        usage = TokenUsage(
            history_tokens=sum(
                message.token_count
                for message in tokenized_history
            ),
            context_tokens=sum(
                chunk.token_count
                for chunk in tokenized_chunks
            ),
        )

        usage.total_tokens = (
            usage.history_tokens
            + usage.context_tokens
        )

        logger.info(
            f"Context window built successfully "
            f"({usage.total_tokens} prompt tokens)."
        )

        # ---------------------------------------------------------
        # Step 9 - Return prepared context
        # ---------------------------------------------------------

        return ContextWindow(
            context=context,
            history=[
                message.message
                for message in tokenized_history
            ],
            token_budget=budget,
            token_usage=usage,
        )