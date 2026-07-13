from abc import ABC, abstractmethod

from app.schemas.document import Document


class DocumentFilterPipeline(ABC):

    @abstractmethod
    async def filter(
        self,
        document: Document,
    ) -> Document:
        raise NotImplementedError