from loguru import logger

def multiply_node(state):
    try:
        result = state.intermediate_result
        multiplier = state.numbers[-1]

        final = result * multiplier

        logger.info(f"Multiply: {result} * {multiplier} = {final}")

        return {
            "final_result": final,
            "steps": state.steps + [{"operation": "multiply", "result": final}]
        }

    except Exception as e:
        logger.error(f"Error in multiply_node: {str(e)}")
        raise