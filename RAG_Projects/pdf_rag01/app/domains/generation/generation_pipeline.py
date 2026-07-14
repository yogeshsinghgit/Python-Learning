from app.api.dependencies.context_window import (
    get_context_window_manager,
)
from app.api.dependencies.llm import (
    get_llm_client,
)
from app.api.dependencies.message_builder import (
    get_message_builder,
)
from app.api.dependencies.prompt import (
    get_prompt_registry,
    get_prompt_renderer,
)
from app.api.dependencies.retrieval import (
    get_retrieval_pipeline,
)
from app.domains.generation.interfaces.pipeline import (
    GenerationPipeline,
)
from app.rag_services.generation.pipeline import (
    DefaultGenerationPipeline,
)
from app.rag_services.generation.response_parser import (
    DefaultResponseParser,
)

_generation_pipeline: GenerationPipeline | None = None


async def get_generation_pipeline() -> GenerationPipeline:
    global _generation_pipeline

    if _generation_pipeline is None:

        retrieval_pipeline = await get_retrieval_pipeline()

        context_window_manager = await get_context_window_manager()

        prompt_registry = await get_prompt_registry()

        prompt_renderer = await get_prompt_renderer()

        message_builder = await get_message_builder()

        llm_client = await get_llm_client()

        response_parser = await get_response_parser()

        _generation_pipeline = DefaultGenerationPipeline(
            retrieval_pipeline=retrieval_pipeline,
            context_window_manager=context_window_manager,
            prompt_registry=prompt_registry,
            prompt_renderer=prompt_renderer,
            message_builder=message_builder,
            llm_client=llm_client,
            response_parser=response_parser,
        )

    return _generation_pipeline