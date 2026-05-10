from loguru import logger

def route_after_planner(state):
    try:
        logger.info(f"Routing based on: {state.operations}")

        if not state.operations:
            logger.warning("No operations identified. Defaulting to answer node.")
            return "answer"

        if "add" in state.operations:
            return "add"

        return "answer"

    except Exception as e:
        logger.error(f"Routing error: {str(e)}")
        raise