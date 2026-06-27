from abc import ABC, abstractmethod


class DenseEmbedder(ABC):

    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> list[float]:
        raise NotImplementedError

    @abstractmethod
    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        raise NotImplementedError