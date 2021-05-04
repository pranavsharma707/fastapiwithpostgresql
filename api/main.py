from fastapi import FastAPI,status
from typing import List,Optional
from databases import Database
from database import engine,SessionLocal,Base,database
import model
from model import notes
from fastapi.middleware.cors import CORSMiddleware
from router import notes


model.metadata.create_all(engine)


app = FastAPI(title = "REST API using FastAPI PostgreSQL Async EndPoints")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(notes.router)
