from langchain_groq import ChatGroq

from app.core.settings import settings
from app.tools.metadata_tool import document_metadata


tools = [
    document_metadata,
]


primary_llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model=settings.GROQ_MODEL_MAIN,
    temperature=0.2,
)

fallback_llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model=settings.GROQ_MODEL_FALLBACK,
    temperature=0.2,
)


llm_with_tools = primary_llm.bind_tools(tools)
fallback_llm_with_tools = fallback_llm.bind_tools(tools)