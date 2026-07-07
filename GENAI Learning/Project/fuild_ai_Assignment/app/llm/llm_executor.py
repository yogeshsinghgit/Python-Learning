from loguru import logger

from app.llm.groq_client import fallback_llm_with_tools, llm_with_tools
from app.core.settings import settings


async def invoke_llm(messages):
    for attempt in range(1, settings.MAX_RETRIES + 1):
        try:
            logger.info(f"Primary LLM attempt {attempt}")

            return await llm_with_tools.ainvoke(messages)

        except Exception as exc:
            logger.exception(
                f"Primary LLM failed on attempt {attempt}: {exc}"
            )

    logger.warning("Switching to fallback model.")

    return await fallback_llm_with_tools.ainvoke(messages)