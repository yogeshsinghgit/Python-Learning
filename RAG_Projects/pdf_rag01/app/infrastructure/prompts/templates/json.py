from app.domains.generation.enums import PromptType
from app.domains.generation.models import PromptTemplate


JSON_V1 = PromptTemplate(
    name="rag.json",
    version="1.0.0",
    prompt_type=PromptType.JSON,
    system_template="""
    Return ONLY valid JSON.

    Do not include markdown.
    """.strip(),
        user_template="""
    Question:
    {query}

    Context:
    {context}
    """.strip(),
    )