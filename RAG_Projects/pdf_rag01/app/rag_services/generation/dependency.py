from app.infrastructure.prompts.default_prompt_renderer import DefaultPromptRenderer
from app.infrastructure.prompts.interfaces.renderer import PromptRenderer
from app.infrastructure.prompts.interfaces.registry import PromptRegistry
from app.infrastructure.prompts.in_memory_registry import InMemoryPromptRegistry
from app.rag_services.generation.content_window.interfaces.token_counter import TokenCounter
from app.rag_services.generation.content_window.token_counter import TikTokenCounter

from app.rag_services.generation.content_window.truncator import (
    DefaultHistoryTruncator
)

from app.rag_services.generation.content_window.interfaces.history_truncator import (
    DefaultHistoryTruncator
)

from app.rag_services.generation.content_window.interfaces.context_truncator import (
    ContextTruncator
)

from app.rag_services.generation.content_window.default_context_truncator import (
    DefaultContextTruncator
)

from app.rag_services.generation.content_window.context_organizers.lost_in_middle_organizer import (
    LostMiddleContextOrganizer
)
from app.rag_services.generation.content_window.interfaces.context_organizer import (
    ContextOrganizer
)

from app.domains.generation.service import GenerationService

from app.api.dependencies.generation_pipeline import (
    get_generation_pipeline,
)


from app.rag_services.generation.interfaces.response_parser import (
    ResponseParser,
)
from app.rag_services.generation.response_parser import (
    DefaultResponseParser,
)


# prompt registry
_prompt_registry = InMemoryPromptRegistry()
async def get_prompt_registry() -> PromptRegistry:
    return _prompt_registry


_prompt_renderer = DefaultPromptRenderer()
async def get_prompt_renderer() -> PromptRenderer:
    return _prompt_renderer


_message_builder = DefaultMessageBuilder()
async def get_message_builder() -> MessageBuilder:
    return _message_builder

# context window management
_token_counter = TikTokenCounter()
async def get_token_counter() -> TokenCounter:
    return _token_counter


_history_truncator = DefaultHistoryTruncator()
async def get_history_truncator() -> HistoryTruncator:
    return _history_truncator


_context_truncator = DefaultContextTruncator()
async def get_context_truncator() -> ContextTruncator:
    return _context_truncator

_context_organizer = LostMiddleContextOrganizer()
async def get_context_organizer() -> ContextOrganizer:
    return _context_organizer


_response_parser = DefaultResponseParser()
async def get_response_parser() -> ResponseParser:
    return _response_parser

async def get_generation_service() -> GenerationService:
    pipeline = await get_generation_pipeline()

    return GenerationService(
        pipeline=pipeline,
    )