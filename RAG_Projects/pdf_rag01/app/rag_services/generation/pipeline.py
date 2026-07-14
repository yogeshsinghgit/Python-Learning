from loguru import logger

from app.domains.generation.models import (
    GenerationRequest,
    GenerationResult,
    PromptVariables,
    LLMRequest,
)
from app.rag_services.generation.content_window.interfaces.pipeline import GenerationPipeline
from app.rag_services.retrieval.pipeline.retrieval_pipeline import RetrievalPipeline
from app.rag_services.generation.content_window.interfaces.manager import ContextWindowManager
from app.infrastructure.prompts.interfaces.registry import PromptRegistry
from app.infrastructure.prompts.interfaces.renderer import PromptRenderer
from app.infrastructure.prompts.interfaces.message_builder import MessageBuilder
from app.rag_services.generation.content_window.interfaces.response_parser import ResponseParser



class DefaultGenerationPipeline(GenerationPipeline):

    def __init__(
        self,
        self,
        retrieval_pipeline: RetrievalPipeline,
        context_window_manager: ContextWindowManager,
        prompt_registry: PromptRegistry,
        prompt_renderer: PromptRenderer,
        message_builder: MessageBuilder,
        llm_client: LLMClient,
        response_parser: ResponseParser,
    ) -> None:

        self._retrieval_pipeline = retrieval_pipeline
        self._context_window_manager = context_window_manager
        self._prompt_registry = prompt_registry
        self._prompt_renderer = prompt_renderer
        self._message_builder = message_builder
        self._llm_client = llm_client
        self._response_parser = response_parser

    async def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResult:

        logger.info(
            f"Generating response for '{request.query}'"
        )

        #
        # Retrieve documents
        #

        retrieval_context = await self._retrieval_pipeline.retrieve(
            query=request.query,
            top_k=request.top_k,
        )

        #
        # Build context window
        #

        context_window = await self._context_window_manager.build(
            history=request.history,
            retrieval_context=retrieval_context,
            max_context_tokens=request.max_context_tokens,
            reserved_response_tokens=request.reserved_response_tokens,
        )

        #
        # Load prompt
        #

        prompt = await self._prompt_registry.get(
            request.prompt_name,
            request.prompt_version,
        )

        #
        # Render prompt
        #

        rendered_prompt = await self._prompt_renderer.render(
            prompt=prompt,
            variables=PromptVariables(
                query=request.query,
                context=context_window.context,
                history="",
            ),
        )

        #
        # Build chat messages
        #

        messages = await self._message_builder.build(
            prompt=rendered_prompt,
            history=context_window.history,
        )

        #
        # Build provider request
        #

        llm_request = LLMRequest(
            messages=messages,
            temperature=request.temperature,
            max_tokens=request.max_response_tokens,
        )

        #
        # Generate
        #

        llm_response = await self._llm_client.generate(
            llm_request
        )

        #
        # Parse
        #

        return await self._response_parser.parse(
            llm_response
        )