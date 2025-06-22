from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
import databases
import sqlalchemy
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/mydb")
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Define a simple notes table
notes = sqlalchemy.Table(
    "notes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("text", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(DATABASE_URL.replace("asyncpg", "psycopg2"))
metadata.create_all(engine)  # Creates table at startup if it doesn't exist

class NoteIn(BaseModel):
    text: str

class NoteOut(NoteIn):
    id: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()

app = FastAPI(lifespan=lifespan)

@app.post("/notes/", response_model=NoteOut)
async def create_note(note: NoteIn):
    query = notes.insert().values(text=note.text)
    note_id = await database.execute(query)
    return {**note.dict(), "id": note_id}

@app.get("/notes/{note_id}", response_model=NoteOut)
async def read_note(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    row = await database.fetch_one(query)
    if row is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return row
