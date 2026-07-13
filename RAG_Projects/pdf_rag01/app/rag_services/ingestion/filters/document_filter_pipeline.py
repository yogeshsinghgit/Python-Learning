from __future__ import annotations

from loguru import logger

from app.rag_services.ingestion.interfaces.element_filter import ElementFilter
from app.rag_services.ingestion.interfaces.document_filter_pipeline import DocumentFilterPipeline
from app.schemas.document import Document


class DefaultDocumentFilterPipeline(DocumentFilterPipeline):
    """
    Executes document filters sequentially.
    """

    def __init__(
        self,
        filters: list[ElementFilter],
    ) -> None:
        self._filters = filters

    async def filter(
        self,
        document: Document,
    ) -> Document:

        logger.info(
            f"Running {len(self._filters)} document filters."
        )

        for element_filter in self._filters:

            before = len(document.elements)

            logger.debug(
                f"Running filter: {element_filter.name}"
            )

            document = await element_filter.filter(document)

            after = len(document.elements)

            logger.debug(
                f"{element_filter.name}: "
                f"{before} -> {after}"
            )

        logger.info(
            f"Document filtering completed. "
            f"Remaining elements: {len(document.elements)}"
        )

        return document