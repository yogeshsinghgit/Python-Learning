import sys

from loguru import logger


def configure_logging() -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        level="INFO",
        enqueue=True,
        backtrace=True,
        diagnose=False,
    )

    logger.add(
        "logs/application.log",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        level="DEBUG",
        enqueue=True,
    )