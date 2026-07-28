import os

DB_NAME = "tasks.db"

print("Database path:", os.path.abspath(DB_NAME))

import sqlite3
db_name = "tasks.db" 

def get_connection():
    conn = sqlite3.connect(db_name)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done BOOLEAN NOT NULL CHECK (done IN (0, 1))
    )
    ''')

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_done
        ON tasks(done)
    """)