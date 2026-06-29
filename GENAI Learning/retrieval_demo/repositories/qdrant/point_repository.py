from loguru import logger

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    PointStruct,
    SparseVector,
)

from exceptions.point import PointUploadError
from repositories.interfaces.point_repository import (
    PointRepository,
)
from schemas.point import HybridPoint
from schemas.vectors import DenseVector, SparseVectorData


class QdrantPointRepository(PointRepository):

    def __init__(
        self,
        client: AsyncQdrantClient,
        collection_name: str,
        batch_size: int = 100,
    ) -> None:

        self._client = client
        self._collection_name = collection_name
        self._batch_size = batch_size
        
    @staticmethod
    def _to_point_struct(point: HybridPoint) -> PointStruct:

        return PointStruct(
            id=point.point_id,

            vector={
                "dense": point.dense.values,
                "sparse": SparseVector(
                    indices=point.sparse.indices,
                    values=point.sparse.values,
                ),
            },

            payload=point.payload,
        )

    async def upload_points(self, points: list[HybridPoint]) -> None:

        if not points:
            logger.warning(
                "No points supplied for upload."
            )
            return

        logger.info(
            f"Uploading {len(points)} points."
        )

        try:

            point_structs = [
                self._to_point_struct(point)
                for point in points
            ]

            for start in range(
                0,
                len(point_structs),
                self._batch_size,
            ):

                batch = point_structs[
                    start:start + self._batch_size
                ]

                logger.info(
                    f"Uploading batch of {len(batch)} points."
                )

                await self._client.upsert(
                    collection_name=self._collection_name,
                    points=batch,
                    wait=True,
                )

            logger.success(
                f"Uploaded {len(points)} points successfully."
            )

        except Exception as exc:

            logger.exception(
                f"Point upload failed: {exc}"
            )

            raise PointUploadError(
                "Unable to upload points."
            ) from exc