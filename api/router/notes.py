from fastapi import APIRouter,status,FastAPI,HTTPException
from typing import List,Optional
from databases import Database
from database import engine,SessionLocal,Base,database
import model
from model import notes,users
from starlette.responses import JSONResponse
from starlette.requests import Request
from schema import Note,NoteIn,Email
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from typing import List
router=APIRouter()
app=FastAPI()

@router.on_event("startup")
async def startup():
    await database.connect()

@router.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@router.get("/notes/", response_model=List[Note], status_code = status.HTTP_200_OK)
async def read_notes(skip: int = 0, take: int = 20):
    query =notes.select().offset(skip).limit(take)
    return await database.fetch_all(query)


@router.get("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def read_notes(note_id: int):
    query =notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query)

@router.post("/notes/", response_model=Note, status_code = status.HTTP_201_CREATED)
async def create_note(note: NoteIn):
    query =notes.insert().values(text=note.text, completed=note.completed)
    last_record_id = await database.execute(query)
    return {**note.dict(), "id": last_record_id}

@router.put("/notes/{note_id}/", response_model=Note, status_code = status.HTTP_200_OK)
async def update_note(note_id: int, payload: NoteIn):
    query = notes.update().where(notes.c.id == note_id).values(text=payload.text, completed=payload.completed)
    await database.execute(query)
    return {**payload.dict(), "id": note_id}


@router.delete("/notes/{note_id}/",response_model=Note,status_code = status.HTTP_200_OK)
async def delete_note(note_id: int):
    query =notes.delete().where(notes.c.id == note_id)
    await database.execute(query)
    return {"message": "Note with id: {} deleted successfully!".format(note_id)}

conf = ConnectionConfig(
    MAIL_USERNAME = "javashrm@gmail.com",
    MAIL_PASSWORD = "corejava@1234",
    MAIL_FROM = "javashrm@gmail.com",
    MAIL_PORT = 587,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_TLS = True,
    MAIL_SSL = False,
)

template = """
<p>Your Account is registered Sucessfully </p>
"""

@router.post('/User',   status_code=status.HTTP_200_OK)
async def User_Created(email:Email):
    if not email.email:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="User is not Created")
    else:

    #return {"message":"user created successfully"}
        message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"), # List of recipients, as many as you can pass
        body=template,
        subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail="User is Created Sucessfully")
        last_record_id = await database.execute(query)
        return {**users.dict(), "id": last_record_id}



    
