from loguru import logger
import re

from states import CalculatorState

def parse_node(state: CalculatorState):
    try:
        logger.info(f"Parsing input: {state.user_input}")

        numbers = list(map(int, re.findall(r'\d+', state.user_input)))

        operations = []
        if "add" in state.user_input:
            operations.append("add")
        if "multiply" in state.user_input:
            operations.append("multiply")

        logger.info(f"Extracted numbers: {numbers}, operations: {operations}")

        return {
            "numbers": numbers,
            "operations": operations
        }

    except Exception as e:
        logger.error(f"Error in parse_node: {str(e)}")
        raise


def add_node(state: CalculatorState):
    try:
        a, b = state.numbers[0], state.numbers[1]

        logger.info(f"Adding {a} + {b}")

        result = a + b

        return {
            "intermediate_result": result,
            "steps": state.steps + [{"operation": "add", "result": result}]
        }

    except Exception as e:
        logger.error(f"Error in add_node: {str(e)}")
        raise


def multiply_node(state: CalculatorState):
    try:
        result = state.intermediate_result
        multiplier = state.numbers[-1]

        logger.info(f"Multiplying {result} * {multiplier}")

        final = result * multiplier

        return {
            "final_result": final,
            "steps": state.steps + [{"operation": "multiply", "result": final}]
        }

    except Exception as e:
        logger.error(f"Error in multiply_node: {str(e)}")
        raise


def answer_node(state: CalculatorState):
    try:
        logger.info(f"Generating final answer")

        return {
            "final_result": state.final_result or state.intermediate_result
        }

    except Exception as e:
        logger.error(f"Error in answer_node: {str(e)}")
        raise