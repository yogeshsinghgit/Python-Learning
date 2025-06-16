import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
import databases
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/mydb")
database = databases.Database(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    for i in range(10):  # retry 10 times
        try:
            await database.connect()
            break
        except Exception as e:
            print(f"DB connection failed (attempt {i+1}/10): {e}")
            await asyncio.sleep(2)
    else:
        raise RuntimeError("Database connection failed after retries")

    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
