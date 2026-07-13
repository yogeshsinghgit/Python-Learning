from collections import defaultdict

from loguru import logger

from app.domains.generation.models import PromptTemplate


class InMemoryPromptRegistry(PromptRegistry):

    def __init__(self) -> None:
        self._prompts: dict[str, dict[str, PromptTemplate]] = defaultdict(dict)

    async def register(self, prompt: PromptTemplate) -> None:

        logger.info(
            f"Registering prompt '{prompt.name}' version '{prompt.version}'"
        )

        self._prompts[prompt.name][prompt.version] = prompt

    async def get(
        self,
        name: str,
        version: str = "latest",
    ) -> PromptTemplate:

        versions = self._prompts.get(name)

        if versions is None:
            raise ValueError(f"Prompt '{name}' not found.")

        if version == "latest":

            latest = sorted(versions.keys())[-1]

            logger.debug(
                f"Loading latest version '{latest}' for prompt '{name}'"
            )

            return versions[latest]

        if version not in versions:
            raise ValueError(
                f"Prompt '{name}' version '{version}' not found."
            )

        return versions[version]

    async def exists(
        self,
        name: str,
        version: str = "latest",
    ) -> bool:

        try:
            await self.get(name, version)
            return True

        except Exception:
            return False

    async def list(self) -> list[PromptTemplate]:
        return [
            prompt
            for versions in self._prompts.values()
            for prompt in versions.values()
        ]


_prompt_registry = InMemoryPromptRegistry()


async def get_prompt_registry() -> PromptRegistry:
    return _prompt_registry