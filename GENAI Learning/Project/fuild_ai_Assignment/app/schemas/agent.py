from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    request: str = Field(..., min_length=5)


class AgentResponse(BaseModel):
    status: str
    message: str