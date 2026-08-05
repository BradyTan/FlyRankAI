from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import RequestValidationError
from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
import sqlite3
data = [
        ("Sample Task 1", 0),
        ("Sample Task 2", 0),
        ("Sample Task 3", 0)
]
with sqlite3.connect("tasks.db") as connection:
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title text NOT NULL,
        done BOOLEAN NOT NULL CHECK (done IN (0,1)));
    """)
    cursor.execute("PRAGMA journal_mode=WAL;")
    if cursor.execute("SELECT * FROM tasks").rowcount == 0:
        cursor.executemany("INSERT INTO tasks (title, done) VALUES (?, ?);", data)
        connection.commit()
app = FastAPI()

memory = { 0: {
    "id": 0,
    "title": "Sample Task",
    "done": False
    }
         , 1: {
    "id": 1,
    "title": "Sample Task 2",
    "done": False
    }
         , 2: {
    "id": 2,
    "title": "Sample Task 3",
    "done": False
    }}
backup_memory = memory.copy()

class Task(BaseModel):
    title: Optional[str] = None
    id: Optional[int] = None
    done: Optional[bool] = None

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"error": exc.errors(), "body": exc.body}),
    )
@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/tasks")
async def search_tasks(search: str | None = None, done: bool | None = None):
    result = ()
    if search is None and done is None:
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks")
            result = cursor.fetchall()
    elif search is not None and done is not None:
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM tasks WHERE title LIKE ? AND done = ?;", (f"%{search}%", int(done)))
            result = cursor.fetchall()
    else:
        with sqlite3.connect("tasks.db") as connection:
            cursor = connection.cursor()
            if search is not None:
                cursor.execute("SELECT * FROM tasks WHERE title LIKE ?;", (f"%{search}%",))
            elif done is not None:
                cursor.execute("SELECT * FROM tasks WHERE done = ?;", (int(done),))
            result = cursor.fetchall()
    return  result



@app.get("/tasks/{id}")
async def get_task(id: int):
    with sqlite3.connect("tasks.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?;", (id,))
        task = cursor.fetchone()
        if task is None:
            return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
        return task

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/tasks", status_code=201)
async def create_task(task: Task):
    if task.title is None:
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    if str(task.title).strip("{}") == "":
        return JSONResponse(status_code=400, content={"error": "Task cannot be empty"})
    with sqlite3.connect("tasks.db") as connection:
        cursor = connection.cursor()
        cursor.execute("BEGIN;")
        cursor.execute("INSERT INTO tasks (title, done) VALUES (?, ?);", (task.title, False))
        connection.commit()
        return {"id": cursor.lastrowid, "title": task.title, "done": False}

@app.put("/tasks/{id}")
async def update_task(task: Task):
    print(task.done)
    if task.title == None and task.done == None:
        return JSONResponse(status_code=400, content={"error": "Task title or done status is required"})
    for task_id in memory:
        if memory[task_id]["id"] == task.id:
            if task.title != None:
                memory[task_id]["title"] = task.title
            if task.done != None:
                memory[task_id]["done"] = task.done
            return memory[task_id]
    return JSONResponse(status_code=404, content={"error": f"Task {task.id} not found"}) 

@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    for task_id in memory:
        if memory[task_id]["id"] == id:
            del memory[task_id]
            return {"message": "No Content"}
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.get("/stats")
async def get_stats():
    total_tasks = len(memory)
    incomplete_tasks = len([task for task in memory.values() if not task["done"]])
    completed_tasks = total_tasks - incomplete_tasks
    return { "total": total_tasks, "done": completed_tasks, "open": incomplete_tasks}
@app.post("/reset", status_code=204)
async def reset_tasks():
    global memory
    memory = backup_memory.copy()
    return {"message": "Reset successful"}