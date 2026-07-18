from psycopg import AsyncConnection
from psycopg.rows import dict_row

from app.core.config import settings


_connection: AsyncConnection | None = None


async def connect_postgres() -> AsyncConnection:

    global _connection

    if _connection is None:

        _connection = await AsyncConnection.connect(
            conninfo=settings.postgres_url.replace(
                "postgresql+asyncpg",
                "postgresql",
            ),
            row_factory=dict_row,
            autocommit=True,
        )

    return _connection


async def disconnect_postgres():

    global _connection

    if _connection:

        await _connection.close()

        _connection = None