from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exception_handlers import RequestValidationError
from fastapi import FastAPI, Request
from typing import Optional
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
    if task.title is None:
        return JSONResponse(status_code=400, content={"error": "Task title is required"})
    if str(task.title).strip("{}") == "":
        return JSONResponse(status_code=400, content={"error": "Task cannot be empty"})
    index = len(memory) + 1
    memory[index] = {
        "id": index,
        "title": task.title,
        "done": False
    }
    return memory[index]

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