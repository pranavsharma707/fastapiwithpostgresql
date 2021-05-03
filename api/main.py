from fastapi import FastAPI,status
from typing import List,Optional
from databases import Database
from database import engine,SessionLocal,Base,database
import model
from model import notes
from schema import Note,NoteIn
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()

model.metadata.create_all(engine)


app = FastAPI(title = "REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/notes/", response_model=List[Note], status_code = status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query =notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)

@app.get("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def read_notes(note_id: int):
    query =notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)

@app.post("/notes/", response_model=Note, status_code = status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query =notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

@app.put("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}

@app.delete("/notes/{note_id}/", status_code = status.HTTP_200_OK)
async def delete_note(note_id: int):
    query =notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(note_id)}

