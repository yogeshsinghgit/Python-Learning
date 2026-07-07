from pydantic import BaseModel, Field


class PromptModel(BaseModel):
    """Represents the prompt sent to an LLM."""

    system_prompt: str = Field(
        ...,
        description="System level instruction."
    )

    user_prompt: str = Field(
        ...,
        description="User prompt containing query and context."
    )