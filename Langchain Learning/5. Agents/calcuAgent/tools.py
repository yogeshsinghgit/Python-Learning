import json
from langchain.tools import tool
from loguru import logger


@tool
def add_numbers(input: str) -> int:
    """
    Adds two numbers.

    The input must be a JSON string like:
    {"a": 10, "b": 5}
    """

    try:
        logger.info(f"Raw tool input received: {input}")

        data = json.loads(input)

        a = int(data["a"])
        b = int(data["b"])

        logger.info(f"Parsed values: a={a}, b={b}")

        result = a + b

        logger.success(f"Addition result: {result}")

        return result

    except Exception as e:
        logger.exception(f"Error in add_numbers tool: {e}")
        raise


@tool
def multiply_numbers(input: str) -> int:
    """
    Multiplies two numbers.

    The input must be a JSON string like:
    {"a": 15, "b": 3}
    """

    try:
        logger.info(f"Raw tool input received: {input}")

        data = json.loads(input)

        a = int(data["a"])
        b = int(data["b"])

        logger.info(f"Parsed values: a={a}, b={b}")

        result = a * b

        logger.success(f"Multiplication result: {result}")

        return result

    except Exception as e:
        logger.exception(f"Error in multiply_numbers tool: {e}")
        raise