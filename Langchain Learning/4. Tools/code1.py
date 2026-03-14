from langchain.tools import tool
from langchain_groq import ChatGroq
from loguru import logger
import os

from dotenv import load_dotenv
load_dotenv()
# create tool
@tool
def multiply_numbers(a: int, b: int) -> int:
    """Multiply two numbers"""

    try:
        logger.info(f"Multiplying {a} and {b}")
        return a * b
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)

llm_with_tools = llm.bind_tools([multiply_numbers])


response = llm_with_tools.invoke(
    "What is 45 multiplied by 78?"
)

# Step 1: check if tool call exists
if response.tool_calls:

    tool_call = response.tool_calls[0]

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    logger.info(f"Tool requested: {tool_name} with {tool_args}")

    # Step 2: execute tool
    result = multiply_numbers.invoke(tool_args)

    logger.info(f"Tool result: {result}")

    # Step 3: send result back to model
    final_response = llm_with_tools.invoke(
        f"The result of multiply_numbers is {result}. Explain the answer."
    )

    print(final_response.content)