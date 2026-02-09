"""
File: main.py
Function: The entry point of the application.
Goals:
1. Initialize the FastAPI application.
2. Orchistrate the CRUD logic. (Create, read, update, delete)
3. Define the API endpoints (URL routes) that the frontend will call.
4. Intergrate the database models with the API logic.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import SQLModel, Session
from database import engine
from models import TODO
from typing import Annotated

# Handle database setup on startup and cleanup on shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

# Opens a session for each API request. 
def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(lifespan=lifespan)

# Create a new TODO item in the database and return the saved record
@app.post("/todos/")
def create_todo(todo: TODO, session: SessionDep):
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
    
