from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    qdrant_url: str = "http://localhost:6333"

    collection_name: str = "fastapi_docs"

    embedding_dimension: int = 384


settings = Settings()