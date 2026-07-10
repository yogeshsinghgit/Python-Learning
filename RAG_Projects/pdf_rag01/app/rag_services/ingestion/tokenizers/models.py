
from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TokenizationResult(BaseModel):
    """
    Result returned by a TokenCounter implementation.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    # Number of tokens.
    token_count: int

    # Optional token ids.
    # Needed by chunk splitters.
    token_ids: list[int] = Field(default_factory=list)