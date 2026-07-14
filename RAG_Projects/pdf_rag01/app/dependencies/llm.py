from app.infrastructure.llm.grok_client import GrokClient
from app.infrastructure.llm.interfaces.client import LLMClient

_llm_client: LLMClient | None = None


async def get_llm_client() -> LLMClient:
    global _llm_client

    if _llm_client is None:
        _llm_client = GrokClient()

    return _llm_client