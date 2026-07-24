from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import init_db, get_connection

app = FastAPI()
@app.on_event("startup")
def startup():
    init_db()
    
class TaskCreate(BaseModel):
    title:str

class TaskUpdate(BaseModel):
    title:str
    done:bool


@app.get("/",summary="Get API information")
def root():
    return {
    "name":"Task API",
    "version":"1.0.0",
    "endpoints":["/tasks"]
    }

@app.get("/health",summary="Check server health")
def health():
    return {"status":"ok"}

@app.get("/tasks",summary="Get all tasks")
def get_tasks():
    return tasks

tasks  = [
    {
        "id":1,
        "title":"Networks assignment",
        "done":False
    },
    {
        "id":2,
        "title":"Project review AI",
        "done":True
    },
    {
        "id":3,
        "title":"Prepare for coding exam",
        "done":False
    }
]

@app.get("/tasks/{id}",summary="Get a task by id")
def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(
        status_code=404, 
        detail={"error": f"Task {id} not found"})

@app.post("/tasks", status_code = 201, summary="Create a new task")
def create_task (task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400,
                            detail = "Title cannot be empty")

    new_task = {
        "id":len(tasks)+1,
        "title": task.title,
        "done":False
    }

    tasks.append(new_task)
    return new_task

@app.put("/tasks/{id}",summary="Update a task")
def update_task(id: int, updated_task: TaskUpdate):
    if not updated_task.title.strip():
        raise HTTPException(status_code=400,
                            detail = "Title cannot be empty")
    for task in tasks:
        if task["id"] == id:
            task["title"] = updated_task.title
            task["done"] = updated_task.done
            return task

    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.delete("/tasks/{id}",status_code=204,summary="Delete a task")
def delete_task(id:int):
    for index, task in enumerate(tasks):
        if task["id"]==id:
            tasks.pop(index)
            return Response(status_code=204)

    raise HTTPException(status_code=404, detail=f"Task {id} not found")

@app.get("/stats", summary="Get task statistics")
def get_stats():
    total = len(tasks)
    done = sum(task["done"] for task in tasks)
    open_tasks = total - done

    return {
        "total": total,
        "done": done,
        "open": open_tasks
    }

tasks = tasks.copy()
@app.post("/reset")
def reset():

    global tasks

    tasks = tasks.copy()

    return {
        "message":"Tasks reset successfully"
    }