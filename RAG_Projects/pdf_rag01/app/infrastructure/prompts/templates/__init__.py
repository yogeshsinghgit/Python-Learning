from app.infrastructure.prompts.templates.citation import CITATION_V1
from app.infrastructure.prompts.templates.evaluation import EVALUATION_V1
from app.infrastructure.prompts.templates.json import JSON_V1
from app.infrastructure.prompts.templates.rag import RAG_V1

ALL_PROMPTS = [
    RAG_V1,
    CITATION_V1,
    JSON_V1,
    EVALUATION_V1,
]