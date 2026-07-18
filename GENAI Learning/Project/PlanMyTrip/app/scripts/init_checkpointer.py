from psycopg import connect

DATABASE_URL = (
    "postgresql://postgres:postgres@localhost:5432/travel_agent"
)

with connect(DATABASE_URL, autocommit=True) as conn:

    from langgraph.checkpoint.postgres import PostgresSaver

    checkpointer = PostgresSaver(conn)

    checkpointer.setup()

print("Checkpoint tables created.")