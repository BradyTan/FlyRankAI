from fastapi.responses import JSONResponse
from fastapi import FastAPI
from typing import Any, Optional
from pydantic import BaseModel
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

class Task(BaseModel):
    title: str

    
@app.get("/")
async def root():
    return {"Hello": "World"}

@app.get("/tasks")
async def get_tasks():
    return memory

@app.get("/tasks/{id}")
async def get_task(id: int):
    for task_id in memory:
        if memory[task_id]["id"] == id:
            return memory[task_id]
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/tasks", status_code=201)
async def create_task(task: Task):
    print(task)
    if task is None or not task.title:
        return JSONResponse(status_code=400, content={"error": "Task must have a title"})
    
    if str(task.title).strip("{}") == "":
        return JSONResponse(status_code=400, content={"error": "Task cannot be empty"})
    index = len(memory)
    print(task.title)
    memory[index] = {
        "id": index,
        "title": task.title,
        "done": False
    }
    return memory[index]