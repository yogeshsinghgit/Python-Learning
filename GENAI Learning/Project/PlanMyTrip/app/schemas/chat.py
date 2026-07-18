from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    thread_id: str = Field(
        ...,
        description="Unique conversation identifier.",
        examples=["user-123"],
    )

    message: str = Field(
        ...,
        min_length=1,
        description="User message.",
        examples=["Plan a 5 day Goa trip"],
    )


class ChatResponse(BaseModel):
    response: str