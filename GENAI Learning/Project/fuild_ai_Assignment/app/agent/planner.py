from loguru import logger

from app.prompts.system_prompt import PLANNER_SYSTEM_PROMPT
from app.llm.groq_client import primary_llm

from app.schemas.plan import ExecutionPlan


async def create_execution_plan(user_request: str) -> ExecutionPlan:
    logger.info("Creating execution plan...")

    messages = [
        (
            "system",
            PLANNER_SYSTEM_PROMPT,
        ),
        (
            "human",
            f"""
        User Request:

        {user_request}
        """,
        ),
    ]

    planner = primary_llm.with_structured_output(ExecutionPlan)
    execution_plan = await planner.ainvoke(messages)

    logger.info(
        f"Generated {len(execution_plan.tasks)} execution tasks."
    )

    logger.info("Task List")
    for task in execution_plan.tasks:
        logger.info(f"{task.id}. {task.title}")

    return execution_plan