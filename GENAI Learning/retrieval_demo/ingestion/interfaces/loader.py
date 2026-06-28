from abc import ABC, abstractmethod
from pathlib import Path

from schemas.document import Document


class Loader(ABC):

    @abstractmethod
    async def load(
        self,
        path: Path,
    ) -> Document:
        raise NotImplementedError