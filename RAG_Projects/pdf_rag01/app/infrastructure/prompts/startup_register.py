from loguru import logger

from app.infrastructure.prompts.templates import ALL_PROMPTS


async def register_prompts(
    registry: PromptRegistry,
) -> None:

    for prompt in ALL_PROMPTS:

        await registry.register(prompt)

    logger.success(
        f"Registered {len(ALL_PROMPTS)} prompts."
    )