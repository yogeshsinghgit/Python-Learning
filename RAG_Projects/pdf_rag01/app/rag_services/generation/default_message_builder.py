from loguru import logger

from app.domains.generation.enums import MessageRole
from app.domains.generation.models import (
    ChatMessage,
    RenderedPrompt,
)

from app.infrastructure.prompts.interfaces.message_builder import MessageBuilder


class DefaultMessageBuilder(MessageBuilder):

    async def build(
        self,
        prompt: RenderedPrompt,
        history: list[ChatMessage],
    ) -> list[ChatMessage]:

        logger.debug("Building chat messages.")

        messages: list[ChatMessage] = [
            ChatMessage(
                role=MessageRole.SYSTEM,
                content=prompt.system_prompt,
            )
        ]

        messages.extend(history)

        messages.append(
            ChatMessage(
                role=MessageRole.USER,
                content=prompt.user_prompt,
            )
        )

        logger.debug(
            f"Built {len(messages)} messages."
        )

        return messages