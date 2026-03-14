

from langchain_core.prompts import ChatPromptTemplate
from loguru import logger


def chat_prompt_example():

    try:

        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an AI assistant that answers questions in a concise manner."),
            ("human", "{question}")
        ])

        messages = chat_prompt.format_messages(
            question="What is LangChain?"
        )

        logger.info(f"Formatted Messages: {messages}")

        print(messages)

    except Exception as e:
        logger.error(f"Error formatting chat prompt: {e}")
        raise


chat_prompt_example()