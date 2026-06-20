from pydantic import BaseModel

class Chunk(BaseModel):
    chunk_id: str
    document_id: str
    chunk_index: int
    content: str
    chunk_size: int