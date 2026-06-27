from abc import ABC, abstractmethod


class CollectionRepository(ABC):

    @abstractmethod
    async def verify_connection(self) -> None:
        ...

    @abstractmethod
    async def collection_exists(self) -> bool:
        ...

    @abstractmethod
    async def create_collection(self) -> None:
        ...

    @abstractmethod
    async def delete_collection(self) -> None:
        ...

    @abstractmethod
    async def close(self) -> None:
        ...