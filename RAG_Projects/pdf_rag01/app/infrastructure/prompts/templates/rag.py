from app.domains.generation.enums import PromptType
from app.domains.generation.models import PromptTemplate


RAG_V1 = PromptTemplate(
    name="rag.answer",
    version="1.0.0",
    prompt_type=PromptType.RAG,
    description="Default production RAG prompt.",
    tags=["rag", "citation", "production"],
    system_template="""
        You are a helpful AI assistant.

        Answer ONLY from the provided context.

        If the answer cannot be found, say you don't know.

        Always be factual.

        Never hallucinate.
        """.strip(),
            user_template="""
        Question:
        {query}

        Context:
        {context}
        """.strip(),
        )