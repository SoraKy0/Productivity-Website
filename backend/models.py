"""
File: Models.py
Function: Defines the structure of the database tables (Blueprints)
Goals:
1. Use SQLAlchemy to map python classes to database tables.
2. Define the "TODO" model with fields: id, title, and completed status.
2. Ensure the database knows exactly what data to expect. 
"""
from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

# Contains the fields that all TODO models will have. To avoid repeating code.
class TODOBase(SQLModel):
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=600)
    position: int = Field(default=0) # Pos of TODO in list.
    priority: int = Field(default=0) # There will be 3 levels of priority. (0 = No priority, 1 = Low, 2 = Medium, 3 = High)

# This is what the user sends to the API when creating a new TODO.
class TODOCreate(TODOBase):
    pass

# This is what we send to the user screen. It gurantees id and timestamp will be included in the data to the frontend.
class TODOPublic(TODOBase):
    id: int
    timestamp: datetime

# This is the actual SQL table in the database.
class TODO(TODOBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) # Automatically set the timestamp to the current time when a new TODO is created