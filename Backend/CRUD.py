from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import RequestValidationError
from fastapi import FastAPI, Request
from typing import Optional
from pydantic import BaseModel
import psycopg
import os
from dotenv import load_dotenv
load_dotenv()
data = [
        ("Sample Task 1", False),
        ("Sample Task 2", False),
        ("Sample Task 3", False)
]
DATABASE_URL = os.getenv('DATABASE_URL')
with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id serial PRIMARY KEY,
            title text NOT NULL,
            created_at text default CURRENT_TIMESTAMP,
            updated_at text default CURRENT_TIMESTAMP,
            done boolean NOT NULL);
        """)
        if not cur.execute("SELECT 1 FROM tasks LIMIT 1").fetchone():
            cur.executemany("INSERT INTO tasks (title, done) VALUES (%s, %s);", data)
            conn.commit()
        
app = FastAPI()
class Task(BaseModel):
    title: Optional[str] = None
    id: Optional[int] = None
    done: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

class Create_Task(BaseModel):
    title: Optional[str] = None
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
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tasks")
                result = cur.fetchall()
    elif search is not None and done is not None:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM tasks WHERE title LIKE %s AND done = %s;", (f"%{search}%", int(done)))
                result = cur.fetchall()
    else:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                if search is not None:
                    cur.execute("SELECT * FROM tasks WHERE title LIKE %s;", (f"%{search}%",))
                elif done is not None:
                    cur.execute("SELECT * FROM tasks WHERE done = %s?;", (int(done),))
                result = cur.fetchall()
    return  result
@app.get("/sort")
async def sort():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks ORDER BY title")
            return cur.fetchall()


@app.get("/tasks/{id}")
async def get_task(id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM tasks WHERE id = %s;", (id,))
            task = cur.fetchone()
            if task is None:
                return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
            return task

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/tasks", status_code=201)
async def create_task(task: Create_Task):
    if task.title is None:
        return JSONResponse(status_code=400, content={"error": "Title is required"})
    if str(task.title).strip("{}") == "":
        return JSONResponse(status_code=400, content={"error": "Task cannot be empty"})
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING *;", (task.title, False))
            conn.commit()
            return cur.fetchone()

            

@app.put("/tasks/{id}")
async def update_task(task: Task):
    if task.title == None or task.done == None or task.id == None or task.created_at == None or task.updated_at == None:
        return JSONResponse(status_code=400, content={"error": "Invalid body"})
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("BEGIN;")
                cur.execute("UPDATE tasks SET title = %s, done = %s, created_at = %s, updated_at = %s WHERE id = %s RETURNING *;", (task.title, task.done, task.created_at, task.updated_at , task.id))
                conn.commit()
                if cur.rowcount > 0 and cur.rowcount is not None:
                    return cur.fetchone()
                else:
                    return JSONResponse(status_code=404, content={"error": f"Task {task.id} not found"})   
            except Exception as e:
                conn.rollback()
                return JSONResponse(status_code=500, content={"error": f"Unable to update task: {e}"}) 

@app.delete("/tasks/{id}", status_code=204)
async def delete_task(id: int):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute("BEGIN;")
                cur.execute("DELETE FROM tasks WHERE id = %s;",(id,))
                conn.commit()
                if cur.rowcount > 0 and cur.rowcount is not None:
                    return {"message": "No Content"}
                else:
                    return JSONResponse(status_code=404, content={"error":"Unknown id"})
            except Exception as e:
                conn.rollback()
                return JSONResponse(status_code=500, content={"error": f"Unable to delete the task: {e}"})
    

@app.get("/stats")
async def get_stats():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            total_tasks = cur.execute("SELECT COUNT(*) FROM tasks;").fetchone()[0]
            incomplete_tasks = cur.execute("SELECT COUNT(*) FROM tasks WHERE done = False;").fetchone()[0]
            completed_tasks = total_tasks - incomplete_tasks
            return { "total": total_tasks, "done": completed_tasks, "open": incomplete_tasks}
@app.post("/reset", status_code=204)
async def reset_tasks():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("DROP TABLE tasks")
            conn.commit()
            cur.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id serial PRIMARY KEY,
                title text NOT NULL,
                created_at text default CURRENT_TIMESTAMP,
                updated_at text default CURRENT_TIMESTAMP,
                done boolean NOT NULL);
            """)
            if not cur.execute("SELECT 1 FROM tasks LIMIT 1").fetchone():
                cur.executemany("INSERT INTO tasks (title, done) VALUES (%s, %s);", data)
                conn.commit()

        