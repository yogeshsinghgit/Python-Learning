from loguru import logger

import sys
from pathlib import Path
# Add the parent directory of 'app' to the search path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.data.documents import DOCUMENTS
from app.services.embedding_service import (
    EmbeddingService,
)
from app.services.similarity_service import (
    SimilarityService,
)



def main() -> None:

    embedding_service = EmbeddingService()

    query = "Which database stores data in memory?"
    query = "Where can I store relational data?"
    # Python API framework
    # Document oriented database
    logger.info(f"Running for query {query}")
    query_embedding = (
        embedding_service.generate_embedding(
            query
        )
    )

    best_document = ""
    best_score = -1.0

    for document in DOCUMENTS:

        document_embedding = (
            embedding_service.generate_embedding(
                document
            )
        )

        score = (
            SimilarityService.cosine_similarity(
                query_embedding,
                document_embedding,
            )
        )

        logger.info(
            f"Document: {document}"
        )

        logger.info(
            f"Similarity Score: {score}"
        )

        if score > best_score:
            best_score = score
            best_document = document

    logger.success(
        f"Most Relevant Document: {best_document}"
    )

    logger.success(
        f"Best Score: {best_score}"
    )


if __name__ == "__main__":
    main()