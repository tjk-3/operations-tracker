import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "operations.db"

def connect_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn

def create_projects_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_name TEXT NOT NULL,
    company_name TEXT,
    client_name TEXT,
    status TEXT,
    priority TEXT,
    due_date DATE,
    assigned_to TEXT,
    next_action TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
""")
    conn.commit()
    conn.close()