from pydantic import BaseModel


class EmbeddedChunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    vector: list[float]