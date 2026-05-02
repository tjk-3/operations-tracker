import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = BASE_DIR / "data" / "operations.db"

def connect_db():
    DB_NAME.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_NAME)

#CREATE TABLES
#clients
def create_clients_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        company_name TEXT,
        phone TEXT,
        email TEXT UNIQUE
    )
    """
    conn.execute(query)
    conn.commit()
    print("Clients table created!")

#projects
def create_projects_table(conn):
    query = """
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        client_id INTEGER NOT NULL,
        total_price REAL,
        status TEXT,
        due_date DATE,
        notes TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    """
    conn.execute(query)
    conn.commit()
    print("Projects table created!")

#payments
def create_payments_table(conn):
    query = """
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
    """
    conn.execute(query)
    conn.commit()
    print("Payments table created!")

#CLIENT FUNCTIONS
#INSERT
def insert_clients(conn, client_name:str, company_name:str, phone:str, email:str):
    query = "INSERT INTO clients (client_name, company_name, phone, email) VALUES (?, ?, ?, ?)"
    conn.execute(query, (client_name, company_name, phone, email))
    conn.commit()
    print(f"{client_name} inserted!")
#SEARCH
def fetch_clients(conn, condition: str = None) -> list[tuple]:
    query = "SELECT * FROM clients"
    if condition:
        query += f" WHERE {condition}"
    try:
        with conn:
            rows = conn.execute(query).fetchall()
        return rows
    except Exception as e:
        print(e)
#DELETE
def delete_clients(conn, client_id:int, ):
    query = "DELETE FROM clients WHERE id = ?"
    try:
        with conn:
            conn.execute(query, (client_id,))
        print(f"Deleted client ID {client_id} from the database!")
    except Exception as e:
        print(e)
#UPDATE
def update_clients(conn, client_id: int, client_name: str, company_name: str, phone: str, email: str):
    current_client = conn.execute(
        "SELECT client_name, company_name, phone, email FROM clients WHERE id = ?",
        (client_id,)
    ).fetchone()

    if current_client is None:
        print(f"No client found with ID {client_id}")
        return

    old_name, old_company, old_phone, old_email = current_client

    changes = []

    new_name = client_name if client_name else old_name
    if client_name and client_name != old_name:
        changes.append(f"name → {client_name}")

    new_company = company_name if company_name else old_company
    if company_name and company_name != old_company:
        changes.append(f"company → {company_name}")

    new_phone = phone if phone else old_phone
    if phone and phone != old_phone:
        changes.append(f"phone → {phone}")

    new_email = email if email else old_email
    if email and email != old_email:
        changes.append(f"email → {email}")

    query = """
    UPDATE clients
    SET client_name = ?, company_name = ?, phone = ?, email = ?
    WHERE id = ?
    """

    with conn:
        conn.execute(query, (new_name, new_company, new_phone, new_email, client_id))

    if changes:
        print(f"Updated client {client_id}: " + ", ".join(changes))
    else:
        print("No changes made.")
#ADD MANY
def insert_many_clients(conn, clients:list[tuple[str, str, str, str]]):
    query = "INSERT INTO clients (client_name, company_name, phone, email) VALUES (?, ?, ?, ?)"
    try:
        with conn:
            conn.executemany(query, clients)
        print(f"Inserted {len(clients)} clients into database!")
    except Exception as e:
        print(e)



def main():
    conn = connect_db()

    create_clients_table(conn)
    create_projects_table(conn)
    create_payments_table(conn)

    while True:
        start = input("Enter Option (Add Client, Delete Client, Update Client, Search Clients, Add Many Clients)\n").lower()
        if start == 'add client':
            client_name = input("Enter Client Name: ")
            company_name = input("Enter Company Name: ")
            phone = input("Enter Phone Number (xxx-xxx-xxxx):")
            email = input("Enter Email: ")
            insert_clients(conn, client_name, company_name, phone, email)

        elif start == 'delete client':
            client_id = input("Enter Client ID: ")
            delete_clients(conn, client_id)

        elif start == 'search clients':
            print("Search Results:")
            for clients in fetch_clients(conn):
                print(clients)

        elif start == 'update client':
            client_id = input("Enter Client ID to update: ")
            client_name = input("Enter updated Client Name, or press Enter to keep existing: ")
            company_name = input("Enter updated Company Name, or press Enter to keep existing: ")
            phone = input("Enter updated Phone Number, or press Enter to keep existing: ")
            email = input("Enter updated Email, or press Enter to keep existing: ")

            update_clients(conn, client_id, client_name, company_name, phone, email)


        elif start == 'add many clients':
            clients = []
            count = int(input("How many clients do you want to add? "))
            for i in range(count):
                print(f"\nClient {i + 1}")
                client_name = input("Name: ")
                company_name = input("Company: ")
                phone = input("Phone: ")
                email = input("Email: ")

                clients.append((client_name, company_name, phone, email))

            insert_many_clients(conn, clients)

        elif start == "exit":
            print("Bye!")
            break


    conn.close()


if __name__ == "__main__":
    main()