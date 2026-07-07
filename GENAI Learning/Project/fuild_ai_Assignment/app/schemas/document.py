from pydantic import BaseModel


class GeneratedSection(BaseModel):
    task_id: int
    title: str
    content: str