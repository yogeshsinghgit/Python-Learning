from typing import Any

from pydantic import BaseModel

from app.domains.generation.models import ChatMessage


class LLMRequest(BaseModel):
    messages: list[ChatMessage]

    temperature: float = 0.2

    max_tokens: int = 1024

    top_p: float = 1.0

    stream: bool = False


class LLMResponse(BaseModel):
    content: str

    finish_reason: str | None = None

    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    raw_response: dict[str, Any] | None = None