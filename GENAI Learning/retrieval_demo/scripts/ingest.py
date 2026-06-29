import asyncio
import sys
from pathlib import Path

# Ensure the project root (retrieval_demo/) is on sys.path so that
# 'core', 'services', etc. are importable regardless of where this
# script is invoked from.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.container import Container
from core.logger import configure_logger

# Resolve docs/ relative to the project root (retrieval_demo/),
# so the script works correctly no matter which directory you run it from.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_FILE = PROJECT_ROOT / "docs" / "fastapi.md"


async def main() -> None:

    configure_logger()

    container = Container()

    try:

        await container.ingestion_service.ingest(
            DOCS_FILE,
        )

    finally:

        await container.collection_repository.close()


if __name__ == "__main__":
    asyncio.run(main())
