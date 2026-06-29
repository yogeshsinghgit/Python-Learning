from itertools import batched
from pathlib import Path

from loguru import logger

from ingestion.builders.point_builder import PointBuilder
from ingestion.interfaces.chunker import Chunker
from ingestion.interfaces.loader import Loader
from repositories.interfaces.collection_repository import (
    CollectionRepository,
)
from repositories.interfaces.point_repository import (
    PointRepository,
)


class IngestionService:

    def __init__(
        self,
        loader: Loader,
        chunker: Chunker,
        collection_repository: CollectionRepository,
        point_repository: PointRepository,
        point_builder: PointBuilder,
        batch_size: int,
    ) -> None:

        self._loader = loader
        self._chunker = chunker
        self._collection_repository = collection_repository
        self._point_repository = point_repository
        self._point_builder = point_builder
        self._batch_size = batch_size

    async def ingest(
        self,
        markdown_file: Path,
    ) -> None:

        logger.info(
            f"Starting ingestion for '{markdown_file.name}'."
        )

        await self._collection_repository.verify_connection()

        await self._collection_repository.create_collection()

        document = await self._loader.load(
            markdown_file,
        )

        chunks = await self._chunker.chunk(
            document,
        )

        logger.info(
            f"Generated {len(chunks)} chunks."
        )

        total_uploaded = 0

        for chunk_batch in batched(
            chunks,
            self._batch_size,
        ):

            chunk_batch = list(chunk_batch)

            logger.info(
                f"Processing batch of {len(chunk_batch)} chunks."
            )

            points = await self._point_builder.build_batch(
                chunk_batch,
            )

            await self._point_repository.upload_points(
                points,
            )

            total_uploaded += len(points)

        logger.success(
            f"Ingestion completed successfully."
        )

        logger.success(
            f"Uploaded {total_uploaded} chunks."
        )