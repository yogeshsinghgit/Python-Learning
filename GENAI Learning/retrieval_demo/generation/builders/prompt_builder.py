from pathlib import Path

from loguru import logger

from generation.models.context import ContextModel
from generation.models.prompt import PromptModel
from generation.prompts.system_prompt import SYSTEM_PROMPT


class PromptBuilder:
    """Builds prompts for the LLM."""
    def build(
        self,
        query: str,
        context: ContextModel,
    ) -> PromptModel:

        logger.info(
            f"Building prompt using {context.chunk_count} chunks."
        )

        user_prompt = f"""
        Context:

        {context.context}

        ------------------------------------------------------------

        Question:

        {query}
        """.strip()

        return PromptModel(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )