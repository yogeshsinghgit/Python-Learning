from fastapi import APIRouter
from loguru import logger

from app.agent.orchestrator import run_agent
from app.schemas.agent import AgentRequest

router = APIRouter(
    prefix="/agent",
    tags=["Agent"],
)


@router.post("")
async def execute_agent(request: AgentRequest):
    try:
        state = await run_agent(request.request)

        return {
            "status": "success",
            "goal": state.execution_plan.goal,
            "tasks": [
                task.model_dump()
                for task in state.execution_plan.tasks
            ],
            "document_path": state.document_path,
        }

    except Exception as exc:
        logger.exception(f"Agent execution failed: {exc}")
        raise

# @router.post(
#     "",
#     response_model=AgentResponse,
# )
# async def execute_agent(request: AgentRequest) -> AgentResponse:
#     try:
#         logger.info(f"Received request: {request.request}")

#         return AgentResponse(
#             status="success",
#             message="Agent execution started.",
#         )

#     except Exception as exc:
#         logger.exception(f"Agent execution failed: {exc}")
#         raise