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
  

class TODOBase(SQLModel):
    """
    PURPOSE: The Blueprint.
    POINT: To avoid repeating yourself. It contains fields that never change regardless
    of whether you are creating, reading, or storing data.
    HOW: Centralizes maintenance so you only update fields like 'title' in one place.
    """
    title: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=600)
    position: int = Field(default=0)
    priority: int = Field(default=0)

class TODOCreate(TODOBase):
    """
    PURPOSE: The Filter (Input).
    POINT: Security and Simplicity. When a user creates a Todo, we don't want them
    sending an ID or timestamp (the server/DB handles those).
    HOW: It "hides" those internal fields from the API user, asking only for what is necessary.
    """
    pass

class TODOPublic(TODOBase):
    """
    PURPOSE: The Mask (Output).
    POINT: Data Guarantee. The frontend (React/Vue) needs the ID to edit or delete
    items later.
    HOW: By setting 'id: int', we promise the frontend that every item returned
    will definitely include its ID and timestamp.
    """
    id: int
    timestamp: datetime

class TODO(TODOBase, table=True):
    """
    PURPOSE: The Reality (Database Table).
    POINT: Storage Logic. This is the only class that actually talks to the hard drive.
    HOW: Uses 'table=True' for SQLAlchemy and includes instructions like 'primary_key'
    and 'default_factory' to auto-generate data.
    """
    id: int | None = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TODOUpdate(SQLModel):
    """
    Used when user wants to change existing TODO.
    """
    title: str | None = None
    description: str | None = None
    position: int | None = None
    priority: int | None = None
