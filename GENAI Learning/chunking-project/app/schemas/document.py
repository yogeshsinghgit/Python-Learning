from pydantic import BaseModel


class Document(BaseModel):
    document_id: str
    file_name: str
    content: str