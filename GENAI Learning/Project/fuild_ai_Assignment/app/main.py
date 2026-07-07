from fastapi import FastAPI
from loguru import logger

from app.api.router import api_router
from app.core.settings import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
async def health_check() -> dict:
    logger.info("Health check endpoint called.")

    return {
        "status": "healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION,
    }