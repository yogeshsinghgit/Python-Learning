from string import Formatter

from loguru import logger

from app.domains.generation.models import (
    PromptTemplate,
    RenderedPrompt,
    PromptVariables
)
from app.infrastructure.prompts.interfaces.renderer import PromptRenderer


class DefaultPromptRenderer(PromptRenderer):

    async def render(
        self,
        prompt: PromptTemplate,
        variables: PromptVariables,
    ) -> RenderedPrompt:

        self._validate(
            prompt.system_template,
            variables,
        )

        self._validate(
            prompt.user_template,
            variables,
        )

        logger.debug(
            f"Rendering prompt '{prompt.name}' "
            f"version '{prompt.version}'"
        )

        return RenderedPrompt(
            system_prompt=prompt.system_template.format(**variables),
            user_prompt=prompt.user_template.format(**variables),
        )

    def _validate(
        self,
        template: str,
        variables: dict[str, object],
    ) -> None:

        formatter = Formatter()

        required_fields = {
            field_name
            for _, field_name, _, _
            in formatter.parse(template)
            if field_name
        }

        missing_fields = required_fields - variables.keys()

        if missing_fields:
            raise ValueError(
                f"Missing prompt variables: {sorted(missing_fields)}"
            )