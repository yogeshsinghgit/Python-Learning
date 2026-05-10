from loguru import logger

def answer_node(state):
    try:
        logger.info("Generating final answer")

        if state.final_result is not None:
            return {"final_result": state.final_result}
        elif state.intermediate_result is not None:
             return {"final_result": state.intermediate_result}
        else:
            logger.warning("No result found in state")
            return {"final_result": "Error: Could not calculate a result. Please ensure planning was successful."}

    except Exception as e:
        logger.error(f"Error in answer_node: {str(e)}")
        raise