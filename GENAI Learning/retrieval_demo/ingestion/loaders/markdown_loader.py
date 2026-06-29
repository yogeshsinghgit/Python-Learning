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
            logger.error(
                f"Markdown file not found: {path}"
            )
            raise FileNotFoundError(
                f"{path} does not exist."
            )

        if path.suffix.lower() != ".md":
            logger.error(
                f"Unsupported file type: {path.suffix}"
            )
            raise ValueError(
                "Only markdown (.md) files are supported."
            )

        try:
            async with aiofiles.open(
                path,
                mode="r",
                encoding="utf-8",
            ) as file:
                content = await file.read()

            document = Document(
                document_id=str(uuid4()),
                source=path,
                content=content,
                metadata={
                    "file_name": path.name,
                    "extension": path.suffix,
                },
            )

            logger.success(
                f"Loaded '{path.name}' successfully."
            )

            return document

        except Exception as exc:
            logger.exception(
                f"Failed to load markdown file: {exc}"
            )
            raise