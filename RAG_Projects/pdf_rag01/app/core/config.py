from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    app_name: str = "PDF RAG"

    pinecone_api_key: str = Field(alias="PINECONE_API_KEY")
    pinecone_index_name: str = Field(alias="PINECONE_INDEX_NAME")
    pinecone_cloud: str = Field(alias="PINECONE_CLOUD")
    pinecone_region: str = Field(alias="PINECONE_REGION")

    vector_db_batch_size: int = Field(
                default=100,
                alias="VECTOR_DB_BATCH_SIZE",
            )

    embedding_model: str = Field(alias="EMBEDDING_MODEL")
    embedding_dimension: int = Field(alias="EMBEDDING_DIMENSION")

    sparse_embedding_model: str = Field(
        alias="SPARSE_EMBEDDING_MODEL",
    )

    embedding_batch_size: int = Field(
        alias="EMBEDDING_BATCH_SIZE",
    )

    normalize_embeddings: bool = Field(
        default=True,
        alias="NORMALIZE_EMBEDDINGS",
    )

    similarity_metric: str = Field(alias="SIMILARITY_METRIC")

    document_loader: str = Field(
    default="unstructured",
    alias="DOCUMENT_LOADER",
    )

    max_chunk_tokens: int = 512
    chunk_overlap_tokens: int = 50

    tokenizer_encoding: str = "cl100k_base"


@lru_cache
def get_settings() -> Settings:
    return Settings()