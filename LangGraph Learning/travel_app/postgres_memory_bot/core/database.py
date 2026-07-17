from psycopg import Connection
from psycopg.rows import dict_row


DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/langgraph"
)


def get_connection() -> Connection:
    return Connection.connect(
        DATABASE_URL,
        row_factory=dict_row,
        autocommit=True,
    )