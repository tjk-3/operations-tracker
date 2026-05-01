from db import create_clients_table, create_projects_table, create_payments_table, insert_client, get_all_clients

def main():
    create_clients_table()
    create_projects_table()
    create_payments_table()

    sample = (
        "sample",
        "sample",
        "sample",
        "sample"
    )

    insert_client(sample)

    print("Client inserted successfully!")

clients = get_all_clients()

for client in clients:
    print(client)

if __name__ == "__main__":
    main()