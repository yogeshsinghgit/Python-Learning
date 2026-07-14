
from app.rag_services.generation.content_window.interfaces.pipeline import GenerationPipeline
from app.domains.generation.models import GenerationRequest, GenerationResult

class GenerationService:

    def __init__(
        self,
        pipeline: GenerationPipeline,
    ):
        self._pipeline = pipeline

    async def generate(
        self,
        request: GenerationRequest,
    ):

        return await self._pipeline.generate(
            request
        )