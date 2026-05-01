import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "data" / "operations.db"


def connect_db():
    DB_NAME.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_NAME)


def create_clients_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        phone TEXT,
        email TEXT,
        notes TEXT
    )
    """)

    conn.commit()
    conn.close()


def create_projects_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        project_address TEXT,
        client_id INTEGER,
        total_price REAL,
        status TEXT,
        due_date DATE,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """)

    conn.commit()
    conn.close()


def create_payments_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        payment_stage TEXT NOT NULL,
        expected_amount REAL,
        received_amount REAL,
        date_received DATE,
        status TEXT,
        notes TEXT,
        FOREIGN KEY (project_id) REFERENCES projects(id)
    )
    """)

    conn.commit()
    conn.close()


def insert_project(project):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO projects (
        project_name,
        project_address,
        client_id,
        total_price,
        status,
        due_date,
        notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, project)

    conn.commit()
    conn.close()

def insert_client(client):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO clients (
        client_name,
        phone,
        email,
        notes
    ) VALUES (?, ?, ?, ?)
    """, client)

    conn.commit()
    conn.close()

def insert_payment(payment):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO payments (
        project_id,
        payment_stage,
        expected_amount,
        received_amount,
        date_received,
        status,
        notes
    ) VALUES (?, ?, ?, ?, ?, ?, ?)
    """, payment)

    conn.commit()
    conn.close()

def get_all_clients():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients")
    rows = cursor.fetchall()

    conn.close()
    return rows