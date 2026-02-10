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
from fastapi import FastAPI, Depends, Query, HTTPException
from sqlmodel import SQLModel, Session, select
from database import engine
from models import TODOCreate, TODOPublic, TODO
from typing import Annotated
from sqlalchemy import func

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

# Count the total number of TODO items in the database for a user and return it
@app.get("/todos/count")
def count_todos(session: SessionDep):
    statement = select(func.count()).select_from(TODO).where(TODO.user_id)
    total = session.exec(statement).one()
    return total

# Create a new TODO item in the database and return the saved record
@app.post("/todos/", response_model=TODOPublic)
def create_todo(todo: TODOCreate, session: SessionDep):
    db_todo = TODO.model_validate(todo)
    
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# Read TODO items from the database with pagination (offset and limit)
@app.get("/todos/", response_model=list[TODOPublic])
def read_todos(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le = 100)] = 100
):
    todos = session.exec(select(TODO).offset(offset).limit(limit)).all()
    return todos