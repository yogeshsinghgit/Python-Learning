from loguru import logger
from graph.builder import build_graph
from states.calculator_state import CalculatorState

def run():
    try:
        graph = build_graph()

        state = CalculatorState(
            user_input="Add 10 and 5 then multiply by 3"
        )

        result = graph.invoke(state)

        logger.info(f"Final Output: {result}")

    except Exception as e:
        logger.error(f"Application error: {str(e)}")


if __name__ == "__main__":
    run()