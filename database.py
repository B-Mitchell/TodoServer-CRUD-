# database.py
from sqlmodel import SQLModel, create_engine
from models import Todo

#SQLite URL -creates a file 'todos.db'
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, echo = True)

# create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)