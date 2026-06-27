from abc import ABC, abstractmethod


class SparseEmbedder(ABC):
    @abstractmethod
    async def embed(
        self,
        text: str,
    ) -> tuple[list[int], list[float]]:
        raise NotImplementedError

    @abstractmethod
    async def embed_batch(
        self,
        texts: list[str],
    ) -> list[tuple[list[int], list[float]]]:
        raise NotImplementedError