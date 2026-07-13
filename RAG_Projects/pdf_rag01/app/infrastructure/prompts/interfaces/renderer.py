from __future__ import annotations

from abc import ABC, abstractmethod

from app.domains.generation.models import (
    PromptTemplate,
    RenderedPrompt,
    PromptVariables
)


class PromptRenderer(ABC):

    @abstractmethod
    async def render(
        self,
        prompt: PromptTemplate,
        variables: PromptVariables,
    ) -> RenderedPrompt:
        ...