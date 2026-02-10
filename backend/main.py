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
from models import TODOCreate, TODOPublic, TODO, TODOUpdate
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


# Create a new TODO item in the database and return the saved record
@app.post("/todos/", response_model=TODOPublic, status_code=201)
def create_todo(todo: TODOCreate, session: SessionDep):
    db_todo = TODO.model_validate(todo)
    # Count todos
    statement = select(func.count()).select_from(TODO)
    total = session.exec(statement).one()
    if total >= 50:
        raise HTTPException(status_code=403, detail="Hey You! Finish your TODO before making more!")

    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo

# --- READ MANY ---
@app.get("/todos/", response_model=list[TODOPublic])
def read_todos(
    session: SessionDep, 
    offset: int = 0, 
    limit: Annotated[int, Query(le=100)] = 100
):
    """Fetch a list of todos (Pagination)."""
    todos = session.exec(select(TODO).offset(offset).limit(limit)).all()
    return todos

# --- READ ONE ---
@app.get("/todos/{todo_id}", response_model=TODOPublic)
def read_todo(todo_id: int, session: SessionDep):
    """Fetch a single todo by its unique ID."""
    todo = session.get(TODO, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.patch("/todos/{todo_id}", response_model=TODOPublic)
def update_todo(todo_id: int, todo: TODOUpdate, session: SessionDep):
    # Update an TODO with new data
    todo_db = session.get(TODO, todo_id)
    if not todo_db:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_data = todo.model_dump(exclude_unset=True)
    todo_db.sqlmodel_update(todo_data)
    session.add(todo_db)
    session.commit()
    session.refresh(todo_db)
    return todo_db

# Delete a TODO
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, session: SessionDep):
    todo = session.get(TODO, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return {"ok": True}