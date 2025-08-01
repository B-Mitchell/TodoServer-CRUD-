from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select
from models import Todo
from database import engine, create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()  # called once on startup
    yield  # do nothing on shutdown (for now)

app = FastAPI(lifespan=lifespan)

# create todo
@app.post("/todos/", response_model=Todo)
def create_todo(todo: Todo):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.get("/todos/", response_model=list[Todo])
def read_todos():
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return todos
    
@app.get("/todos/{todo_id}", response_model=Todo)
def read_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo

@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated: Todo):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo.title = updated.title
        todo.description = updated.description
        todo.completed = updated.completed
        session.commit()
        session.refresh(todo)
        return todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        if not todo:
            raise HTTPException(status_code=404, detail= "Todo not found")
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}
    
