from loguru import logger

def add_node(state):
    try:
        a, b = state.numbers[0], state.numbers[1]

        result = a + b

        logger.info(f"Add: {a} + {b} = {result}")

        return {
            "intermediate_result": result,
            "steps": state.steps + [{"operation": "add", "result": result}]
        }

    except Exception as e:
        logger.error(f"Error in add_node: {str(e)}")
        raise