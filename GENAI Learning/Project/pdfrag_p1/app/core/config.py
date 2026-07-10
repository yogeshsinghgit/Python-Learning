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

    embedding_model: str = Field(alias="EMBEDDING_MODEL")
    embedding_dimension: int = Field(alias="EMBEDDING_DIMENSION")

    similarity_metric: str = Field(alias="SIMILARITY_METRIC")


@lru_cache
def get_settings() -> Settings:
    return Settings()