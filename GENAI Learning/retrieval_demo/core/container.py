from qdrant_client import AsyncQdrantClient

from core.config import get_settings
from repositories.qdrant.collection_repository import (
    QdrantCollectionRepository,
)

from ingestion.sentence_transformers.dense_embedder import (
    SentenceTransformerDenseEmbedder
)
from ingestion.fastembed.sparse_embedder import (
    FastEmbedSparseEmbedder,
)

from ingestion.builders.point_builder import PointBuilder

from repositories.qdrant.point_repository import (
    QdrantPointRepository,
)

from ingestion.services.ingestion_service import (
    IngestionService,
)

class Container:
    def __init__(self) -> None:
        settings = get_settings()

        self.qdrant_client = AsyncQdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key,
        )

        self.collection_repository = QdrantCollectionRepository(
            client=self.qdrant_client,
            collection_name=settings.qdrant_collection,
            dense_vector_size=settings.dense_vector_size,
        )

        self.dense_embedder = SentenceTransformerDenseEmbedder(
            model_name=settings.dense_model,
        )

        self.sparse_embedder = FastEmbedSparseEmbedder(
            model_name=settings.sparse_model,
        )

        self.point_builder = PointBuilder(
            dense_embedder=self.dense_embedder,
            sparse_embedder=self.sparse_embedder,
        )

        self.point_repository = QdrantPointRepository(
            client=self.qdrant_client,
            collection_name=settings.qdrant_collection,
            batch_size=100,
        )

        self.ingestion_service = IngestionService(
            collection_repository=self.collection_repository,
            point_repository=self.point_repository,
            point_builder=self.point_builder,
            batch_size=settings.ingestion_batch_size
        )
