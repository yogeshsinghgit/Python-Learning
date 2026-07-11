"""
Unstructured-backed document loader.

Responsibilities:
- Load a document from disk using the Unstructured library.
- Map raw Unstructured elements into domain DocumentElement objects.
- Populate DocumentMetadata with stable, strongly-typed fields.
- Raise DocumentLoadingError on failure.
"""

from __future__ import annotations

import asyncio
import hashlib
import mimetypes
from pathlib import Path
from uuid import uuid4

from loguru import logger
from unstructured.partition.auto import partition

from app.core.exceptions import DocumentLoadingError
from app.rag_services.ingestion.interfaces.document_loader import DocumentLoader
from app.rag_services.ingestion.mappers.unstructured_mapper import (
    UnstructuredElementMapper,
)
from app.schemas.document import Document, DocumentMetadata


class UnstructuredDocumentLoader(DocumentLoader):
    """
    Production document loader backed by Unstructured.
    """

    async def load(
        self,
        file_path: Path,
    ) -> Document:
        try:
            logger.info(f"Loading document: {file_path}")

            elements = await asyncio.to_thread(
                partition,
                filename=str(file_path),
            )

            mapped_elements = [
                UnstructuredElementMapper.map(element)
                for element in elements
            ]

            logger.info(
                f"Parsed {len(mapped_elements)} semantic elements "
                f"from '{file_path.name}'."
            )

            # Derive stable metadata fields from the file itself
            mime_type, _ = mimetypes.guess_type(str(file_path))
            file_size_bytes = file_path.stat().st_size
            page_count = self._extract_page_count(elements)
            languages = self._extract_languages(elements)
            checksum = await asyncio.to_thread(self._compute_checksum, file_path)

            metadata = DocumentMetadata(
                parser="unstructured",
                filename=file_path.name,
                mime_type=mime_type,
                file_size_bytes=file_size_bytes,
                page_count=page_count,
                languages=languages,
                checksum=checksum,
            )

            return Document(
                document_id=str(uuid4()),
                filename=file_path.name,
                elements=mapped_elements,
                metadata=metadata,
            )

        except Exception as exc:
            logger.exception(
                f"Failed to load document '{file_path}'."
            )

            # raise DocumentLoadingError(
            #     f"Unable to load document: {file_path}"
            # ) from exc

    @staticmethod
    def _extract_page_count(elements: list) -> int | None:
        """
        Derive page count from the highest page_number seen in elements.
        """
        page_numbers = [
            getattr(element.metadata, "page_number", None)
            for element in elements
        ]

        valid_pages = [page for page in page_numbers if page is not None]

        return max(valid_pages) if valid_pages else None

    @staticmethod
    def _extract_languages(elements: list) -> list[str]:
        """
        Collect unique detected languages across all elements.
        """
        seen: set[str] = set()
        for element in elements:
            langs = getattr(element.metadata, "languages", None) or []
            seen.update(langs)
        return sorted(seen)

    @staticmethod
    def _compute_checksum(file_path: Path) -> str:
        """
        Compute SHA-256 checksum of the file for deduplication.
        """
        sha256 = hashlib.sha256()
        with file_path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256.update(chunk)
        return sha256.hexdigest()