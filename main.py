from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import init_db, get_connection

#variable assigning 
app = FastAPI()

#Database initialization
@app.on_event("startup")
def startup():
    init_db()

# Pydantic models for requests
class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: str
    done: bool

#API info endpoint
@app.get("/", summary="Get API information")
def root():
    return {
        "name": "Task API",
        "version": "1.0.0",
        "endpoints": ["/tasks"]
    }

#Server health check endpoint
@app.get("/health", summary="Check server health")
def health():
    return {"status": "ok"}

#GET tasks endpoint
@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

#GET task by id endpoint
@app.get("/tasks/{id}", summary="Get a task by id")
def get_task(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()

    conn.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Task not found"}
        )

    return {
        "id": row["id"],
        "title": row["title"],
        "done": bool(row["done"])
    }

#POST endpoint to create new task
@app.post("/tasks", status_code=201, summary="Create a new task")
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        (task.title, 0)
    )

    conn.commit()

    new_id = cursor.lastrowid

    conn.close()

    return {
        "id": new_id,
        "title": task.title,
        "done": False
    }

#PUT endpoint to update existing task
@app.put("/tasks/{id}", summary="Update a task")
def update_task(id: int, updated_task: TaskUpdate):
    if not updated_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (updated_task.title, int(updated_task.done), id)
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    conn.commit()
    conn.close()

    return {
        "id": id,
        "title": updated_task.title,
        "done": updated_task.done
    }

#DELETE endpoint to delete a task
@app.delete("/tasks/{id}", status_code=204, summary="Delete a task")
def delete_task(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail=f"Task {id} not found")

    conn.commit()
    conn.close()

    return Response(status_code=204)

#GET endpoint for task statistics
@app.get("/stats", summary="Get task statistics")
def get_stats():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
    done = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "done": done,
        "open": total - done
    }

#POST endpoint to reset tasks
@app.post("/reset")
def reset():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks")

    cursor.executemany(
        "INSERT INTO tasks (title, done) VALUES (?, ?)",
        [
            ("Networks assignment", 0),
            ("Project review AI", 1),
            ("Prepare for coding exam", 0)
        ]
    )

    conn.commit()
    conn.close()

    return {
        "message": "Tasks reset successfully"
    }

#GET endpoint to search tasks by title
@app.get("/tasks")
def get_tasks(search: str = None):
    conn = get_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute(
            "SELECT * FROM tasks WHERE title LIKE ?",
            (f"%{search}%",)
        )
    else:
        cursor.execute("SELECT * FROM tasks")

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]

#GET tasks in alphabetical order endpoint
@app.get("/tasks")
def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks ORDER BY title")
    rows = cursor.fetchall()

    conn.close()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "done": bool(row["done"])
        }
        for row in rows
    ]