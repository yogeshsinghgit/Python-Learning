from abc import ABC, abstractmethod

from schemas.chunk import Chunk
from schemas.document import Document


class Chunker(ABC):

    @abstractmethod
    async def chunk(
        self,
        document: Document,
    ) -> list[Chunk]:
        raise NotImplementedError