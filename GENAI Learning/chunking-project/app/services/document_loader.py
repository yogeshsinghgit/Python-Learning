from pathlib import Path
from uuid import uuid4

from loguru import logger

from app.schemas.document import Document


class DocumentLoader:

    async def load_documents(
        self,
        docs_path: str,
    ) -> list[Document]:

        documents: list[Document] = []

        try:
            for file in Path(docs_path).glob("*.md"):

                content = file.read_text(
                    encoding="utf-8"
                )

                document = Document(
                    document_id=str(uuid4()),
                    file_name=file.name,
                    content=content,
                )

                documents.append(document)

                logger.info(
                    f"Loaded document: {file.name}"
                )

            return documents

        except Exception as exc:
            logger.exception(
                f"Failed loading documents: {exc}"
            )
            raise