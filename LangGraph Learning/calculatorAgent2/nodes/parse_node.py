import re
from loguru import logger

def parse_node(state):
    try:
        logger.info(f"Parsing input: {state.user_input}")

        numbers = list(map(int, re.findall(r'\d+', state.user_input)))

        return {"numbers": numbers}

    except Exception as e:
        logger.error(f"Error in parse_node: {str(e)}")
        raise