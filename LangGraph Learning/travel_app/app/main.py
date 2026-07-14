from loguru import logger

from graph.builder import graph


def main() -> None:
    test_queries = [
        # "Hello",
        # "Plan a trip to Japan",
        "Plan a trip to India",
        # "Plan a trip to France",
    ]

    for query in test_queries:
        logger.info("=" * 60)
        logger.info(f"Input: {query}")

        # result = graph.invoke(
        #     {
        #         "user_input": query,
        #     }
        # )
        initial_state = {
            "user_input": "Plan a trip to India",
        }

        logger.info("=" * 80)
        logger.info(f"Input: {initial_state['user_input']}")

        for event in graph.stream(initial_state):
            logger.info(f"{event}")


        logger.success("Graph execution completed")
        # logger.info(f"Final State:\n{result['response']}")


if __name__ == "__main__":
    main()