from pathlib import Path
from uuid import uuid4

import aiofiles
from loguru import logger

from ingestion.interfaces.loader import Loader
from schemas.document import Document


class MarkdownLoader(Loader):

    async def load(
        self,
        path: Path,
    ) -> Document:

        logger.info(
            f"Loading markdown file: {path}"
        )

        if not path.exists():
            raise FileNotFoundError(path)

        async with aiofiles.open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            content = await file.read()

        logger.success(
            f"Loaded markdown file: {path.name}"
        )

        return Document(
            document_id=str(uuid4()),
            source=path,
            content=content,
            metadata={
                "file_name": path.name,
            },
        )