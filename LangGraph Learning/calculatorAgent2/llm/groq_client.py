from langchain_groq import ChatGroq
from loguru import logger
from config.settings import GROQ_API_KEY

def get_llm():
    try:
        llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=GROQ_API_KEY
        )
        logger.info("Groq LLM initialized")
        return llm

    except Exception as e:
        logger.error(f"Error initializing LLM: {str(e)}")
        raise