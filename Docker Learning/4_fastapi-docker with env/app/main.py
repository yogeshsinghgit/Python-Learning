from fastapi import FastAPI
from config import settings

app = FastAPI()

@app.get("/env")
def read_env():
    return {
        "db_url": settings.DATABASE_URL,
        "debug": settings.DEBUG,
    }
