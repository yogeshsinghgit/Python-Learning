from langchain_groq import ChatGroq

from app.core.config import settings


class LLMClient:
    """
    Wrapper around the application's LLM.
    """

    def __init__(self) -> None:
        self._client: ChatGroq | None = None

    async def connect(self) -> None:

        if self._client is not None:
            return

        self._client = ChatGroq(
            model=settings.DEFAULT_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

    async def disconnect(self) -> None:
        # Nothing to dispose today, but keeping a uniform lifecycle.
        self._client = None

    @property
    def client(self) -> ChatGroq:

        if self._client is None:
            raise RuntimeError(
                "LLM is not initialized."
            )

        return self._client