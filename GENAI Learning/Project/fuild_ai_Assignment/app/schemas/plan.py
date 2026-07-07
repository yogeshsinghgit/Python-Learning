from pydantic import BaseModel, Field


class Task(BaseModel):
    id: int = Field(..., description="Task number")
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Task description")


class ExecutionPlan(BaseModel):
    goal: str = Field(..., description="Overall goal")
    tasks: list[Task] = Field(default_factory=list)