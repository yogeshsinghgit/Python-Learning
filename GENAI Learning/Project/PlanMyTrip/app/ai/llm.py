from langchain_groq import ChatGroq

from app.core.config import settings


_llm: ChatGroq | None = None


def get_llm() -> ChatGroq:

    global _llm

    if _llm is None:

        _llm = ChatGroq(
            model=settings.DEFAULT_MODEL,
            api_key=settings.GROQ_API_KEY,
            temperature=settings.TEMPERATURE,
            max_tokens=settings.MAX_TOKENS,
        )

    return _llm