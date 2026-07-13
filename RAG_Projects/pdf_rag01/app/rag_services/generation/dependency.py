from app.infrastructure.prompts.default_prompt_renderer import DefaultPromptRenderer
from app.infrastructure.prompts.interfaces.renderer import PromptRenderer
from app.infrastructure.prompts.interfaces.registry import PromptRegistry
from app.infrastructure.prompts.in_memory_registry import InMemoryPromptRegistry



_prompt_registry = InMemoryPromptRegistry()
async def get_prompt_registry() -> PromptRegistry:
    return _prompt_registry


_prompt_renderer = DefaultPromptRenderer()
async def get_prompt_renderer() -> PromptRenderer:
    return _prompt_renderer



_message_builder = DefaultMessageBuilder()
async def get_message_builder() -> MessageBuilder:
    return _message_builder