from itertools import batched

from loguru import logger

from ingestion.builders.point_builder import PointBuilder
from repositories.interfaces.collection_repository import (
    CollectionRepository,
)
from repositories.interfaces.point_repository import (
    PointRepository,
)
from schemas.chunk import Chunk


class IngestionService:
    def __init__(
        self,
        collection_repository: CollectionRepository,
        point_repository: PointRepository,
        point_builder: PointBuilder,
        batch_size: int,
    ) -> None:
        self._collection_repository = collection_repository
        self._point_repository = point_repository
        self._point_builder = point_builder
        self._batch_size = batch_size

    async def ingest(
        self,
        chunks: list[Chunk],
    ) -> None:

        if not chunks:
            logger.warning("No chunks supplied.")
            return

        logger.info(
            f"Starting ingestion for {len(chunks)} chunks."
        )

        await self._collection_repository.verify_connection()

        await self._collection_repository.create_collection()

        for batch in batched(
            chunks,
            self._batch_size,
        ):

            logger.info(
                f"Processing batch of {len(batch)} chunks."
            )

            points = await self._point_builder.build_batch(
                list(batch),
            )

            await self._point_repository.upload_points(
                points,
            )

        logger.success(
            f"Successfully ingested {len(chunks)} chunks."
        )