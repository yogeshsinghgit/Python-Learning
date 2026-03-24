from dotenv import load_dotenv
import os
from loguru import logger

try:
    logger.info("Loading environment variables")

    load_dotenv()

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in environment variables")

    logger.success("Environment variables loaded successfully")

except Exception as e:
    logger.exception(f"Error loading configuration: {e}")
    raise