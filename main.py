from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/")
def root():
    return {
    "name":"Task API",
    "version":"1.0.0",
    "endpoints":["/tasks"]
    }

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/tasks")
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

@app.get("/tasks/{id}")
def get_task(id:int):
    for task in tasks:
        if task["id"] == id:
            return task
    raise HTTPException(
        status_code=404, 
        detail=f"Task {id} not found")

