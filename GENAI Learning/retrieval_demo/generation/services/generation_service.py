from time import perf_counter

from loguru import logger

from generation.builders.context_builder import ContextBuilder
from generation.builders.prompt_builder import PromptBuilder
from generation.clients.llm_client import LLMClient
from generation.models.generation_request import GenerationRequest
from generation.models.generation_response import GenerationResponse
from retrieval.services.retrieval_service import RetrievalService


class GenerationService:

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        llm_client: LLMClient,
    ) -> None:

        self._retrieval_service = retrieval_service
        self._context_builder = context_builder
        self._prompt_builder = prompt_builder
        self._llm_client = llm_client

    async def generate(
        self,
        request: GenerationRequest,
    ) -> GenerationResponse:

        start = perf_counter()

        logger.info(
            f"Generating response for query: {request.query}"
        )

        try:

            retrieved_chunks = await self._retrieval_service.retrieve(
                query=request.query,
            )

            if not retrieved_chunks:
                logger.warning(
                    f"No documents retrieved for query: {request.query}"
                )

                return GenerationResponse(
                    answer="I couldn't find enough information in the knowledge base to answer your question.",
                    retrieved_chunks=[],
                    prompt=None,
                    model="N/A",
                    latency_ms=(perf_counter() - start) * 1000,
                )

            context = self._context_builder.build(
                retrieved_chunks,
            )

            prompt = self._prompt_builder.build(
                query=request.query,
                context=context,
            )

            llm_result = await self._llm_client.generate(
                prompt=prompt,
            )

            latency = (perf_counter() - start) * 1000

            return GenerationResponse(
                answer=llm_result.answer,
                retrieved_chunks=retrieved_chunks,
                prompt=prompt,
                model=llm_result.model,
                latency_ms=latency,
            )

        except Exception as exc:

            logger.exception(
                f"Generation pipeline failed: {exc}"
            )

            raise