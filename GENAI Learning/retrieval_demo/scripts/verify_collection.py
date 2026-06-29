import asyncio
import json

from loguru import logger
from qdrant_client import AsyncQdrantClient

from core.config import get_settings
from core.logger import configure_logger


async def main() -> None:

    configure_logger()

    settings = get_settings()

    client = AsyncQdrantClient(
        host=settings.qdrant_host,
        port=settings.qdrant_port,
        api_key=settings.qdrant_api_key,
    )

    collection_name = settings.qdrant_collection

    try:

        # ── 1. Total point count ──────────────────────────────────────
        collection_info = await client.get_collection(
            collection_name=collection_name,
        )

        total_points = collection_info.points_count

        logger.info(f"Collection: {collection_name}")
        logger.info(f"Total Points: {total_points}")

        # ── 2. Retrieve first few points ─────────────────────────────
        results, _ = await client.scroll(
            collection_name=collection_name,
            limit=3,
            with_payload=True,
            with_vectors=True,
        )

        if not results:
            logger.warning("No points found in the collection.")
            return

        logger.info(f"\nShowing first {len(results)} point(s):\n")

        for point in results:

            dense_vector = point.vector.get("dense", [])  # type: ignore[union-attr]
            sparse_vector = point.vector.get("sparse")    # type: ignore[union-attr]

            sparse_indices_count = (
                len(sparse_vector.indices)
                if sparse_vector is not None
                else 0
            )
            sparse_values_count = (
                len(sparse_vector.values)
                if sparse_vector is not None
                else 0
            )

            logger.info("─" * 40)
            logger.info(f"Point ID:\n  {point.id}")
            logger.info(f"Dense Vector:\n  {len(dense_vector)} dimensions")
            logger.info(f"Sparse Vector:\n  {sparse_indices_count} indices")
            logger.info(f"             \n  {sparse_values_count} values")
            logger.info(
                f"Payload:\n{json.dumps(point.payload, indent=2, default=str)}"
            )

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
