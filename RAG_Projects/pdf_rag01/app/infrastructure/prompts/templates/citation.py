from app.domains.generation.enums import PromptType
from app.domains.generation.models import PromptTemplate


CITATION_V1 = PromptTemplate(
    name="rag.citation",
    version="1.0.0",
    prompt_type=PromptType.CITATION,
    system_template="""
        Answer using citations.

        Every statement should reference its source.
        """.strip(),
            user_template="""
        Question:
        {query}

        Context:
        {context}
        """.strip(),
)