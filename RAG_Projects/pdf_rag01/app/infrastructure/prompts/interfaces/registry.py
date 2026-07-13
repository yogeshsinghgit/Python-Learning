from __future__ import annotations

from abc import ABC, abstractmethod

from loguru import logger

from app.domains.generation.models import PromptTemplate


class PromptRegistry(ABC):

    @abstractmethod
    async def register(self, prompt: PromptTemplate) -> None:
        ...

    @abstractmethod
    async def get(
        self,
        name: str,
        version: str = "latest",
    ) -> PromptTemplate:
        ...

    @abstractmethod
    async def exists(
        self,
        name: str,
        version: str = "latest",
    ) -> bool:
        ...

    @abstractmethod
    async def list(self) -> list[PromptTemplate]:
        ...