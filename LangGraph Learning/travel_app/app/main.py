from loguru import logger

from graph.builder import graph


def main() -> None:
    initial_state = {
        "user_input": "Plan a trip to Japan"
    }


    logger.info("Starting travel planner graph")

    result = graph.invoke(initial_state)

    logger.success("Graph execution completed")

    logger.info(f"Final state: {result}")


if __name__ == "__main__":
    main()