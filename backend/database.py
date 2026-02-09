"""
File: database.py
Function: Manages the connection between the python code and the SQL database.
Goals:
1. Create a connection to the SQLlite database.
2. Configure how python talks to the database.
3. Create a "Session" which is like a single transaction (opening the database, doing work, and closing it).
"""
from sqlmodel import create_engine


sqlite_file_name = "database.db" # Name of database file
sqlite_url = f"sqlite:///{sqlite_file_name}" # Database URL for SQLModel

connect_args = {"check_same_thread": False} # Configues SQLite to allow multiple threads to access the database (important for FastAPI)
engine = create_engine(sqlite_url, connect_args=connect_args) # Create the engine that connects the code to the database
