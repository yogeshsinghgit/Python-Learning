from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from loguru import logger
from llm.groq_client import get_llm

llm = get_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", """
You are a planning agent for a calculation graph.
Your task is to identify the operations requested in the user input.

Available operations: "add", "multiply", "divide", "subtract".

CRITICAL: 
1. Do NOT perform the calculation yourself.
2. Only return the list of operations in the order they should be performed.
3. If multiple operations are needed, list them all.
4. return ONLY valid JSON in the specified format.

Output format:
{{
  "operations": ["add", "multiply"]
}}
"""),
    ("human", "{input}")
])

parser = JsonOutputParser()

def planner_node(state):
    try:
        logger.info(f"Planning for: {state.user_input}")

        chain = prompt | llm | parser

        result = chain.invoke({"input": state.user_input})

        logger.info(f"Planner output: {result}")

        # Handle both {"operations": [...]} and a direct list if returned
        if isinstance(result, list):
            ops = result
        elif isinstance(result, dict):
            ops = result.get("operations", [])
        else:
            ops = []

        return {"operations": ops}

    except Exception as e:
        logger.error(f"Error in planner_node: {str(e)}")
        raise