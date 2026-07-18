from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.db.postgres_client import connect_postgres

_checkpointer: AsyncPostgresSaver | None = None


async def get_checkpointer() -> AsyncPostgresSaver:

    global _checkpointer

    if _checkpointer is None:

        connection = await connect_postgres()

        _checkpointer = AsyncPostgresSaver(connection)

    return _checkpointer