import psycopg2
from psycopg2 import sql
import csv
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

connection = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

def create_contacts_table():
    sql = """
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL UNIQUE
    )
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        connection.commit()


def insert_contacts_from_csv(file_path):
    sql = "INSERT INTO contacts(name, phone) VALUES(%s, %s) ON CONFLICT (phone) DO NOTHING"
    with connection.cursor() as cursor:
        with open(file_path, newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  
            for row in reader:
                name, phone = row
                cursor.execute(sql, (name, phone))
        connection.commit()


def insert_many_contacts(contact_list):
    sql = "CALL insert_many_contacts(%s, %s)"
    with connection.cursor() as cursor:
        for name, phone in contact_list:
            cursor.execute(sql, (name, phone))
        connection.commit()


def add_contact(name, phone):
    sql = "CALL upsert_contact(%s, %s)"

    with connection.cursor() as cursor:
        cursor.execute(sql, (name, phone))
        connection.commit()


def add_contact_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    add_contact(name, phone)
    print(f"Added contact: {name} - {phone}")


def update_contact_phone(name, new_phone):
    sql = "UPDATE contacts SET phone = %s WHERE name = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, (new_phone, name))
        connection.commit()
        return cursor.rowcount


def update_contact_name(phone, new_name):
    sql = "UPDATE contacts SET name = %s WHERE phone = %s"
    with connection.cursor() as cursor:
        cursor.execute(sql, (new_name, phone))
        connection.commit()
        return cursor.rowcount


def update_contact_from_console():
    choice = input("Update (1) Name or (2) Phone: ")

    if choice == "1":
        phone = input("Enter phone: ")
        new_name = input("Enter new name: ")
        updated_count = update_contact_name(phone, new_name)
    elif choice == "2":
        name = input("Enter name: ")
        new_phone = input("Enter new phone: ")
        updated_count = update_contact_phone(name, new_phone)
    else:
        print("Invalid choice.")
        return

    print(f"Updated {updated_count} contact(s).")


def get_all_contacts():
    sql = "SELECT * FROM contacts ORDER BY name"
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def search_contacts_by_pattern(pattern):
    sql = "SELECT * FROM search_contacts(%s)"

    with connection.cursor() as cursor:
        cursor.execute(sql, (pattern,))
        return cursor.fetchall()


def delete_contact(identifier):
    sql = "CALL delete_contact(%s)"

    with connection.cursor() as cursor:
        cursor.execute(sql, (identifier,))
        connection.commit()
        

def delete_contact_from_console():
    phone = input("Enter phone to delete: ")
    confirm = input(f"Are you sure you want to delete {phone}? (y/n): ")
    if confirm.lower() == "y":
        deleted_count = delete_contact_by_phone(phone)
        print(f"Deleted {deleted_count} contact(s).")
    else:
        print("Deletion cancelled.")


def get_contacts_paginated(limit, offset):
    sql = "SELECT * FROM get_contacts_paginated(%s, %s)"

    with connection.cursor() as cursor:
        cursor.execute(sql, (limit, offset))
        return cursor.fetchall()


def display_contacts(contact_list):
    if not contact_list:
        print("  (no contacts)")
        return
    for contact in contact_list:
        print(f"  [{contact[0]}] {contact[1]} - {contact[2]}")


def main():
    create_contacts_table()

    while True:
        print("\n--- PhoneBook ---")
        print("1. Show all contacts")
        print("2. Add contact (console)")
        print("3. Import contacts from CSV")
        print("4. Search contacts")
        print("5. Update phone by name")
        print("6. Update name by phone")
        print("7. Delete contact by name")
        print("8. Delete contact by phone")
        print("9. Paginated view")
        print("10. Insert many contacts")
        print("0. Exit")

        choice = input("\nChoice: ")

        if choice == "1":
            display_contacts(get_all_contacts())
        elif choice == "2":
            add_contact_from_console()
        elif choice == "3":
            file_path = input("Enter CSV file path: ")
            insert_contacts_from_csv(file_path)
        elif choice == "4":
            pattern = input("Search pattern: ")
            display_contacts(search_contacts_by_pattern(pattern))
        elif choice == "5":
            name = input("Enter name: ")
            new_phone = input("Enter new phone: ")
            update_contact_phone(name, new_phone)
        elif choice == "6":
            phone = input("Enter phone: ")
            new_name = input("Enter new name: ")
            update_contact_name(phone, new_name)
        elif choice == "7":
            identifier = input("Enter name or phone: ")
            delete_contact(identifier)
        elif choice == "8":
            delete_contact_from_console()
        elif choice == "9":
            limit = int(input("Limit: "))
            offset = int(input("Offset: "))
            display_contacts(get_contacts_paginated(limit, offset))
        elif choice == "10":
            n = int(input("How many contacts: "))
            data = []
            for _ in range(n):
                name = input("Name: ")
                phone = input("Phone: ")
                data.append((name, phone))
            insert_many_contacts(data)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()
    print("Thank you! Goodbye!")


if __name__ == "__main__":
    main()