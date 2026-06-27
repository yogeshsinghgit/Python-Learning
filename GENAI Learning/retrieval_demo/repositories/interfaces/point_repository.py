from abc import ABC, abstractmethod

from schemas.point import HybridPoint


class PointRepository(ABC):

    @abstractmethod
    async def upload_points(
        self,
        points: list[HybridPoint],
    ) -> None:
        raise NotImplementedError