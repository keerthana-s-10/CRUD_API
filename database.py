import os
from dotenv import load_dotenv
import psycopg
from psycopg.rows import dict_row

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg.connect(
        DATABASE_URL,
        row_factory=dict_row
    )

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL
        )
    """)

    # Create index
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_tasks_done
        ON tasks(done)
    """)

    # Seed only if table is empty
    cursor.execute("SELECT COUNT(*) AS count FROM tasks")
    count = cursor.fetchone()["count"]

    if count == 0:
        cursor.executemany(
            """
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            """,
            [
                ("Networks assignment", False),
                ("Project review AI", False),
                ("Prepare for coding exam", False),
            ],
        )

    conn.commit()
    cursor.close()
    conn.close()