from app.domains.generation.enums import PromptType
from app.domains.generation.models import PromptTemplate


EVALUATION_V1 = PromptTemplate(
    name="rag.evaluation",
    version="1.0.0",
    prompt_type=PromptType.EVALUATION,
    system_template="""
Evaluate the answer quality.
""".strip(),
    user_template="""
Question:
{query}

Answer:
{answer}

Context:
{context}
""".strip(),
)