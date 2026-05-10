from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    logger.error("GROQ_API_KEY is missing in .env")
    raise ValueError("Missing GROQ_API_KEY")

logger.info("Environment variables loaded successfully")