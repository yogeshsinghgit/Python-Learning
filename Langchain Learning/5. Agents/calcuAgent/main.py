from langchain.agents import AgentExecutor
from loguru import logger

from agent import get_agent


def run_agent():

    try:
        logger.info("Loading agent configuration")

        agent, tools = get_agent()

        logger.info("Creating AgentExecutor")

        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )

        logger.success("AgentExecutor initialized successfully")

        # user_query = "What is (10 + 5) * 3 ?"
        user_query = "First add 10 and 5, then multiply the result by 3."

        logger.info(f"User query received: {user_query}")

        response = agent_executor.invoke(
            {"input": user_query}
        )

        logger.success(f"Final response: {response['output']}")

    except Exception as e:
        logger.exception(f"Agent execution failed: {e}")
        raise


if __name__ == "__main__":
    run_agent()