import asyncio
import sys
from pathlib import Path

# Ensure the project root (retrieval_demo/) is on sys.path so that
# 'core', 'services', etc. are importable regardless of where this
# script is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from loguru import logger
from core.dependency import get_retrieval_service
from core.container import Container
from core.logger import configure_logger

# Resolve docs/ relative to the project root (retrieval_demo/),
# so the script works correctly no matter which directory you run it from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

QUERY = "What is OAuth2 authentication?"


async def main() -> None:
    service = get_retrieval_service()

    logger.info(f"Running hybrid retrieval for query: '{QUERY}'")

    results = await service.retrieve(
        query=QUERY,
        top_k=5,
    )

    logger.info(f"Retrieved {len(results)} chunks.")

    print("\n" + "=" * 100)
    print("HYBRID SEARCH RESULTS")
    print("=" * 100)

    for index, chunk in enumerate(results, start=1):
        print(f"\nResult #{index}")
        print(f"Score : {chunk.score:.4f}")
        print(f"Chunk : {chunk.id}")

        source = chunk.metadata.get("source", "Unknown")
        print(f"Source: {source}")

        print("-" * 100)
        print(chunk.content)
        print("-" * 100)


if __name__ == "__main__":
    asyncio.run(main())