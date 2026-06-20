from uuid import uuid4

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from loguru import logger

from app.schemas.chunk import Chunk
from app.schemas.document import Document


class ChunkingService:

    def __init__(
        self,
        chunk_size: int = 500,
        chunk_overlap: int = 50,
    ) -> None:

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    async def create_chunks(
        self,
        document: Document,
    ) -> list[Chunk]:

        try:

            logger.info(
                f"Creating chunks for "
                f"{document.file_name}"
            )

            chunks: list[str] = (
                self._splitter.split_text(
                    document.content
                )
            )

            result: list[Chunk] = []

            for index, chunk_text in enumerate(chunks):

                result.append(
                    Chunk(
                        chunk_id=str(uuid4()),
                        document_id=document.document_id,
                        chunk_index=index,
                        content=chunk_text,
                        chunk_size=len(chunk_text),
                    )
                )

            logger.info(
                f"Created {len(result)} chunks "
                f"for {document.file_name}"
            )

            return result

        except Exception as exc:

            logger.exception(
                f"Chunking failed: {exc}"
            )

            raise