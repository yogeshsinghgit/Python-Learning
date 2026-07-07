from loguru import logger

from app.prompts.system_prompt import EXECUTOR_SYSTEM_PROMPT
from app.llm.llm_executor import invoke_llm
from app.tools.metadata_tool import document_metadata
from app.schemas.document import GeneratedSection
from app.schemas.plan import Task


async def execute_task(
    user_request: str,
    task: Task,
) -> GeneratedSection:
    logger.info(f"Executing task {task.id}: {task.title}")

    messages = [
        (
            "system",
            EXECUTOR_SYSTEM_PROMPT,
        ),
        (
            "human",
            f"""
        User Request:
        {user_request}

        Task Title:
        {task.title}

        Task Description:
        {task.description}

        Generate only this section.
        """,
                ),
            ]


    response = await invoke_llm(messages)

    if response.tool_calls:
        messages.append(response)
        
        from langchain_core.messages import ToolMessage
        for tool_call in response.tool_calls:
            if tool_call["name"] == "document_metadata":
                metadata = document_metadata.invoke(tool_call["args"])
                logger.info(f"{metadata}")
                messages.append(ToolMessage(content=metadata, tool_call_id=tool_call["id"]))
        
        response = await invoke_llm(messages)

    logger.success(f"Completed task {task.id}")

    return GeneratedSection(
        task_id=task.id,
        title=task.title,
        content=response.content,
    )