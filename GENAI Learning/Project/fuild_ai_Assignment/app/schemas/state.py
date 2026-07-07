from pydantic import BaseModel, Field

from app.schemas.document import GeneratedSection
from app.schemas.plan import ExecutionPlan

from pydantic import BaseModel, Field

from app.schemas.document import GeneratedSection
from app.schemas.plan import ExecutionPlan


class AgentState(BaseModel):
    user_request: str

    execution_plan: ExecutionPlan | None = None

    generated_sections: list[GeneratedSection] = Field(
        default_factory=list
    )

    document_path: str | None = None