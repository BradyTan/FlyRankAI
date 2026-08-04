from fastapi.responses import JSONResponse
from fastapi import FastAPI

app = FastAPI()

memory = { 1: {
    "id": 0,
    "title": "Sample Task",
    "done": False
    }
         , 2: {
    "id": 1,
    "title": "Sample Task 2",
    "done": False
    }
         , 3: {
    "id": 2,
    "title": "Sample Task 3",
    "done": False
    }}

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