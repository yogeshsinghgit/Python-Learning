from __future__ import annotations

from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field

from app.domains.generation.enums import (
    MessageRole,
    PromptStatus,
    PromptType,
)


class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))

    role: MessageRole

    content: str

    name: str | None = None

    metadata: dict[str, Any] = Field(default_factory=dict)

class PromptTemplate(BaseModel):
    name: str
    version: str

    prompt_type: PromptType

    system_template: str
    user_template: str

    description: str | None = None

    tags: list[str] = Field(default_factory=list)

    metadata: dict[str, Any] = Field(default_factory=dict)

    status: PromptStatus = PromptStatus.ACTIVE

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )


class RenderedPrompt(BaseModel):
    system_prompt: str
    user_prompt: str


class TokenBudget(BaseModel):
    max_context_tokens: int

    reserved_response_tokens: int

    system_tokens: int = 0

    history_tokens: int = 0

    rag_context_tokens: int = 0

    user_tokens: int = 0

    remaining_tokens: int = 0


class ContextWindow(BaseModel):
    messages: list[ChatMessage]

    token_budget: TokenBudget


class Citation(BaseModel):
    document_id: str

    chunk_id: str

    page_number: int | None = None

    score: float | None = None


class UsageMetrics(BaseModel):
    prompt_tokens: int = 0

    completion_tokens: int = 0

    total_tokens: int = 0

    latency_ms: float = 0.0

    estimated_cost: float = 0.0


class StructuredOutput(BaseModel):
    data: dict[str, Any]


class PromptVariables(BaseModel):
    query: str

    context: str = ""

    conversation_history: str = ""

    answer: str = ""

    metadata: dict[str, Any] = Field(default_factory=dict)

class GenerationRequest(BaseModel):
    query: str

    retrieval_context: str

    conversation_history: list[ChatMessage] = Field(default_factory=list)

    prompt_name: str = "rag.answer"

    prompt_version: str = "latest"

    metadata: dict[str, Any] = Field(default_factory=dict)


class GenerationResult(BaseModel):
    answer: str

    citations: list[Citation] = Field(default_factory=list)

    usage: UsageMetrics | None = None

    raw_response: str | None = None