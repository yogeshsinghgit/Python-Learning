from loguru import logger

from app.agent.executor import execute_task
from app.agent.planner import create_execution_plan
from app.schemas.state import AgentState
from app.services.document_service import generate_document


async def run_agent(user_request: str) -> AgentState:
    logger.info("Starting autonomous agent.")

    state = AgentState(
        user_request=user_request,
    )

    state.execution_plan = await create_execution_plan(
        user_request
    )

    logger.success("Execution plan created.")

    for task in state.execution_plan.tasks:
        section = await execute_task(
            user_request=user_request,
            task=task,
        )

        state.generated_sections.append(section)

    logger.success(
        f"Generated {len(state.generated_sections)} sections."
    )

    state.document_path = await generate_document(state)

    logger.success("Agent execution completed.")

    return state