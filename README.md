# Task API
A simple CRUD REST API built with *FastAPI* as part of my FlyRank AI Backend Internship(Week 2).

## Features
- Get API information
- Health check endpoint
- View all tasks
- View a task by ID
- Create a new task
- Update an existing task
- Delete a task
- Input validation and HTTP status codes
- Interactive API documentation with Swagger UI

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Pydantic

## Screenshot
<img width="1917" height="1078" alt="image" src="https://github.com/user-attachments/assets/ae8375bf-017f-4785-9c75-ff7593ba9875" />

## curl.exe output
<img width="1277" height="142" alt="image" src="https://github.com/user-attachments/assets/f9e56851-0be3-41d1-a70c-c9fbca0168dd" />

## SQLite Database

- This project uses SQLite because it is:
A lightweight, file-based database.
Requires zero server setup or installation.
Stores data in a single tasks.db file.

- Database File
The database file is tasks.db.
It is created automatically when the application starts.
If the file does not exist, the application creates it, creates the tasks table, and seeds three example tasks.
tasks.db is usually added to .gitignore so every clone starts with a fresh database.

- Running the Project:
uvicorn main:app --reload

- Link:
http://127.0.0.1:8000/docs

- SQL Query Example:
SELECT COUNT(*) FROM tasks;
Result: Returns the total number of tasks currently stored in the database.

##DB Browser for SQLite Screenshot 
![db_browser_ss](image.png)