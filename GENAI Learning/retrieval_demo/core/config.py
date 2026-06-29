from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    qdrant_host: str = Field(default="localhost")
    qdrant_port: int = Field(default=6333)
    qdrant_api_key: str | None = Field(default=None)

    qdrant_collection: str = Field(default="knowledge_base")

    dense_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2"
    )
    dense_vector_size: int = Field(default=384)
    sparse_model: str = Field(
        default="Qdrant/bm25"
    )

    chunk_size: int = Field(default=500)

    chunk_overlap: int = Field(default=100)

    ingestion_batch_size: int = Field(default=100)

    log_level: str = Field(default="INFO")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()