from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.domains.ingestion.router import router as ingestion_router

from app.infrastructure.vector_db.pinecone_manager import (
    PineconeManager,
)

from app.infrastructure.embeddings.dense.sentence_transformer import (
    SentenceTransformerDenseEmbedder,
)
from app.infrastructure.embeddings.sparse.fastembed_sparse import (
    FastEmbedSparseEmbedder,
)
from app.infrastructure.embeddings.providers import state


@asynccontextmanager
async def lifespan(app: FastAPI):

    state.dense_embedder = SentenceTransformerDenseEmbedder()

    state.sparse_embedder = FastEmbedSparseEmbedder()

    manager = PineconeManager()

    await manager.create_index()

    await manager.wait_until_ready()

    yield

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.include_router(
    ingestion_router,
)



@app.get("/", tags=["Health"])
async def health_check() -> dict:
    logger.info("Health check endpoint called.")

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }