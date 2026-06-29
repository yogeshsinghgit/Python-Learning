import asyncio
from uuid import uuid4

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
)
from loguru import logger

from ingestion.interfaces.chunker import Chunker
from schemas.chunk import Chunk
from schemas.document import Document


class RecursiveChunker(Chunker):

    def __init__(
        self,
        chunk_size: int,
        chunk_overlap: int,
    ) -> None:

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    async def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:

        logger.info(
            f"Chunking document '{document.source.name}'."
        )

        chunks = await asyncio.to_thread(
            self._splitter.split_text,
            document.content,
        )

        results: list[Chunk] = []

        for index, text in enumerate(chunks):

            results.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    chunk_index=index,
                    document_id=document.document_id,
                    source=document.source,
                    text=text,
                    metadata = {
                        **document.metadata,
                        "chunk_index": index,
                        "source": str(document.source),
                    }
                )
            )

        logger.success(
            f"Generated {len(results)} chunks."
        )

        return results