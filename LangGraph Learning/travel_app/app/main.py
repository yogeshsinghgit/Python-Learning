from loguru import logger

from graph.builder import graph


def main() -> None:
    test_queries = [
        "Hello",
        "Plan a trip to Japan",
        "Plan a trip to India",
        "Plan a trip to France",
    ]

    for query in test_queries:
        logger.info("=" * 60)
        logger.info(f"Input: {query}")

        result = graph.invoke(
            {
                "user_input": query,
            }
        )

        logger.success("Graph execution completed")
        logger.info(f"Final State:\n{result}")


if __name__ == "__main__":
    main()