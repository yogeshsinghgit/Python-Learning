from abc import ABC
from abc import abstractmethod

from generation.models.prompt import PromptModel
from generation.models.result import LLMResult


class LLMClient(ABC):

    @abstractmethod
    async def generate(
        self,
        prompt: PromptModel,
    ) -> LLMResult:
        """Generate an answer from the supplied prompt."""