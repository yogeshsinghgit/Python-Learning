from fastapi import FastAPI
from loguru import logger
from contextlib import asynccontextmanager

from app.core.config import get_settings
from app.domains.ingestion.router import router as ingestion_router
from app.domains.retrieval.router import (
    router as retrieval_router,
)


from app.infrastructure.vector_db.pinecone_manager import (
    PineconeManager,
)
from app.infrastructure.vector_db.pinecone_repository import (
    PineconeRepository
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

    logger.info("Initializing application resources...")

    state.dense_embedder = SentenceTransformerDenseEmbedder()
    state.sparse_embedder = FastEmbedSparseEmbedder()

    manager = PineconeManager()

    await manager.create_index()
    await manager.wait_until_ready()

    state.vector_repository = PineconeRepository()

    logger.success("Application resources initialized.")

    yield

    logger.info("Shutting down application.")

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
app.include_router(
    retrieval_router
)



@app.get("/", tags=["Health"])
async def health_check() -> dict:
    logger.info("Health check endpoint called.")

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }