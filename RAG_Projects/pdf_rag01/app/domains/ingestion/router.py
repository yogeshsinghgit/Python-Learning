from pathlib import Path
import tempfile

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from loguru import logger

from app.domains.ingestion.services import get_document_ingestion_pipeline

from app.rag_services.ingestion.pipeline.document_ingestion_pipeline import (
    DocumentIngestionPipeline,
)

from app.domains.ingestion.models import UploadResponse

router = APIRouter(
    prefix="/documents",
    tags=["Document Ingestion"],
)

@router.post(
    "/upload",
    response_model=UploadResponse,
)
async def upload_document(
    file: UploadFile = File(...),
    pipeline: DocumentIngestionPipeline = Depends(
        get_document_ingestion_pipeline,
    ),
) -> UploadResponse:
    """
    Upload and ingest a PDF document.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    logger.info(
        f"Uploading '{file.filename}'."
    )

    try:
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False,
        ) as tmp:

            contents = await file.read()

            tmp.write(contents)

            temp_path = Path(tmp.name)

        result = await pipeline.ingest(
            temp_path,
        )

        logger.info(
            f"Successfully ingested '{file.filename}'."
        )

        return UploadResponse(
            message="Document ingested successfully.",
            document_id=result.document_id,
            filename=result.filename,
            chunk_count=result.chunk_count,
            vector_count=result.vector_count,
            processing_time_ms=result.processing_time_ms,
        )

    except Exception as exc:

        logger.exception(
            f"Failed to ingest '{file.filename}'."
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )

    finally:

        if temp_path.exists():
            temp_path.unlink(missing_ok=True)