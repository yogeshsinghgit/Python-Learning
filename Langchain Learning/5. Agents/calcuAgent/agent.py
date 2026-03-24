from prompt import prompt
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent
from langchain import hub
from loguru import logger

from config import GROQ_API_KEY
from tools import add_numbers, multiply_numbers


try:
    logger.info("Initializing Groq LLM")

    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0
    )

    logger.success("Groq LLM initialized")

except Exception as e:
    logger.exception(f"Failed to initialize Groq LLM: {e}")
    raise


try:
    logger.info("Registering tools for agent")

    tools = [add_numbers, multiply_numbers]

    logger.success(f"{len(tools)} tools registered")

except Exception as e:
    logger.exception(f"Error registering tools: {e}")
    raise


try:
    logger.info("Loading ReAct agent prompt")

    # prompt = hub.pull("hwchase17/react")
    prompt = prompt

    logger.success("ReAct prompt loaded")

except Exception as e:
    logger.exception(f"Failed to load prompt: {e}")
    raise


try:
    logger.info("Creating ReAct agent")

    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    logger.success("Agent created successfully")

except Exception as e:
    logger.exception(f"Agent creation failed: {e}")
    raise


def get_agent():
    """
    Returns the configured agent and tools.
    """
    return agent, tools