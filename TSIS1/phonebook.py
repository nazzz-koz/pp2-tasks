import psycopg2
import csv
import json
import re
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

connection = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)


def create_tables():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS groups (
            id   SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL
        )
        """,
        """
        INSERT INTO groups (name) VALUES
            ('Family'), ('Work'), ('Friend'), ('Other')
        ON CONFLICT (name) DO NOTHING
        """,
        """
        CREATE TABLE IF NOT EXISTS contacts (
            id       SERIAL PRIMARY KEY,
            name     VARCHAR(255) NOT NULL,
            phone    VARCHAR(20)  NOT NULL UNIQUE,
            email    VARCHAR(100),
            birthday DATE,
            group_id INTEGER REFERENCES groups(id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS phones (
            id         SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES contacts(id) ON DELETE CASCADE,
            phone      VARCHAR(20) NOT NULL,
            type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
        )
        """
    ]
    with connection.cursor() as cursor:
        for q in queries:
            cursor.execute(q)
        connection.commit()


def insert_contacts_from_csv(file_path):
    with connection.cursor() as cursor:
        with open(file_path, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name     = row.get("name", "").strip()
                phone    = row.get("phone", "").strip()
                p_type   = row.get("type", "mobile").strip()
                email    = row.get("email", "").strip() or None
                birthday = row.get("birthday", "").strip() or None
                group    = row.get("group", "").strip()

                if not name or not phone:
                    continue

                group_id = None
                if group:
                    cursor.execute(
                        "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                        (group,)
                    )
                    cursor.execute("SELECT id FROM groups WHERE name = %s", (group,))
                    result = cursor.fetchone()
                    if result:
                        group_id = result[0]

                cursor.execute(
                    """
                    INSERT INTO contacts (name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (phone) DO NOTHING
                    """,
                    (name, phone, email, birthday, group_id)
                )
                cursor.execute("SELECT id FROM contacts WHERE phone = %s", (phone,))
                contact = cursor.fetchone()
                if contact:
                    cursor.execute(
                        "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                        (contact[0], phone, p_type)
                    )
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
    name     = input("Enter name: ")
    phone    = input("Enter phone: ")
    email    = input("Enter email (optional): ").strip() or None
    birthday = input("Enter birthday YYYY-MM-DD (optional): ").strip() or None
    group    = input("Enter group (Family/Work/Friend/Other, optional): ").strip()

    with connection.cursor() as cursor:
        group_id = None
        if group:
            cursor.execute(
                "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                (group,)
            )
            cursor.execute("SELECT id FROM groups WHERE name = %s", (group,))
            result = cursor.fetchone()
            if result:
                group_id = result[0]

        cursor.execute(
            """
            INSERT INTO contacts (name, phone, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (phone) DO UPDATE
                SET name     = EXCLUDED.name,
                    email    = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
            RETURNING id
            """,
            (name, phone, email, birthday, group_id)
        )
        contact_id = cursor.fetchone()[0]
        cursor.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, 'mobile')",
            (contact_id, phone)
        )
        connection.commit()

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
        phone    = input("Enter phone: ")
        new_name = input("Enter new name: ")
        updated_count = update_contact_name(phone, new_name)
    elif choice == "2":
        name      = input("Enter name: ")
        new_phone = input("Enter new phone: ")
        updated_count = update_contact_phone(name, new_phone)
    else:
        print("Invalid choice.")
        return
    print(f"Updated {updated_count} contact(s).")


def get_all_contacts():
    sql = """
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def search_contacts_by_pattern(pattern):
    sql = "SELECT * FROM search_contacts(%s)"
    with connection.cursor() as cursor:
        cursor.execute(sql, (pattern,))
        return cursor.fetchall()


def get_contacts_paginated(limit, offset):
    sql = "SELECT * FROM get_contacts_paginated(%s, %s)"
    with connection.cursor() as cursor:
        cursor.execute(sql, (limit, offset))
        return cursor.fetchall()


def delete_contact(identifier):
    sql = "CALL delete_contact(%s)"
    with connection.cursor() as cursor:
        cursor.execute(sql, (identifier,))
        connection.commit()


def delete_contact_from_console():
    phone   = input("Enter phone to delete: ")
    confirm = input(f"Are you sure you want to delete {phone}? (y/n): ")
    if confirm.lower() == "y":
        delete_contact(phone)
        print("Deleted contact.")
    else:
        print("Deletion cancelled.")


def filter_by_group():
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM groups ORDER BY name")
        groups = cursor.fetchall()

    print("Available groups:")
    for gid, gname in groups:
        print(f"  {gid}: {gname}")

    group_name = input("Enter group name: ").strip()

    sql = """
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON g.id = c.group_id
        WHERE g.name ILIKE %s
        ORDER BY c.name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (f"%{group_name}%",))
        return cursor.fetchall()


def search_by_email():
    email_query = input("Enter email search query: ").strip()
    sql = """
        SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        WHERE c.email ILIKE %s
        ORDER BY c.name
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, (f"%{email_query}%",))
        return cursor.fetchall()


def browse_contacts_paginated():
    order_by = input("Sort by (name / birthday / id) [name]: ").strip() or "name"
    if order_by not in ("name", "birthday", "id"):
        order_by = "name"

    limit  = 5
    offset = 0

    while True:
        sql = f"""
            SELECT c.id, c.name, c.phone, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON g.id = c.group_id
            ORDER BY c.{order_by}
            LIMIT %s OFFSET %s
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, (limit, offset))
            rows = cursor.fetchall()

        display_contacts(rows)

        if not rows:
            print("  No more contacts.")
            break

        cmd = input("\n[n]ext  [p]rev  [q]uit: ").strip().lower()
        if cmd == "n":
            if len(rows) < limit:
                print("Already at last page.")
            else:
                offset += limit
        elif cmd == "p":
            offset = max(0, offset - limit)
        elif cmd == "q":
            break


def add_phone_to_contact():
    name  = input("Enter contact name: ").strip()
    phone = input("Enter phone number: ").strip()
    ptype = input("Enter type (home / work / mobile) [mobile]: ").strip() or "mobile"

    sql = "CALL add_phone(%s, %s, %s)"
    with connection.cursor() as cursor:
        cursor.execute(sql, (name, phone, ptype))
        connection.commit()
    print(f"Phone {phone} ({ptype}) added to {name}.")


def move_contact_to_group():
    name  = input("Enter contact name: ").strip()
    group = input("Enter group name: ").strip()

    sql = "CALL move_to_group(%s, %s)"
    with connection.cursor() as cursor:
        cursor.execute(sql, (name, group))
        connection.commit()
    print(f"Contact '{name}' moved to group '{group}'.")


def export_to_json(file_path):
    sql = """
        SELECT c.id, c.name, c.phone, c.email,
               c.birthday::TEXT, g.name AS group_name
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.name
    """
    contacts = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        for cid, name, phone, email, birthday, group_name in rows:
            cursor.execute(
                "SELECT phone, type FROM phones WHERE contact_id = %s", (cid,)
            )
            phones = [{"phone": p, "type": t} for p, t in cursor.fetchall()]
            contacts.append({
                "name":     name,
                "phone":    phone,
                "email":    email,
                "birthday": birthday,
                "group":    group_name,
                "phones":   phones
            })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)

    print(f"Exported {len(contacts)} contacts to '{file_path}'.")


def import_from_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return

    inserted = skipped = overwritten = 0

    with connection.cursor() as cursor:
        for c in data:
            name     = (c.get("name") or "").strip()
            phone    = (c.get("phone") or "").strip()
            email    = c.get("email") or None
            birthday = c.get("birthday") or None
            group    = (c.get("group") or "").strip()
            phones   = c.get("phones", [])

            if not name or not phone:
                continue

            group_id = None
            if group:
                cursor.execute(
                    "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                    (group,)
                )
                cursor.execute("SELECT id FROM groups WHERE name = %s", (group,))
                result = cursor.fetchone()
                if result:
                    group_id = result[0]

            cursor.execute("SELECT id FROM contacts WHERE phone = %s", (phone,))
            existing = cursor.fetchone()

            if existing:
                choice = input(f'Duplicate phone {phone} ("{name}"). [s]kip / [o]verwrite? ').strip().lower()
                if choice != "o":
                    skipped += 1
                    continue
                contact_id = existing[0]
                cursor.execute(
                    "UPDATE contacts SET name=%s, email=%s, birthday=%s, group_id=%s WHERE id=%s",
                    (name, email, birthday, group_id, contact_id)
                )
                cursor.execute("DELETE FROM phones WHERE contact_id = %s", (contact_id,))
                overwritten += 1
            else:
                cursor.execute(
                    """
                    INSERT INTO contacts (name, phone, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (name, phone, email, birthday, group_id)
                )
                contact_id = cursor.fetchone()[0]
                inserted += 1

            for ph in phones:
                cursor.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                    (contact_id, ph.get("phone"), ph.get("type", "mobile"))
                )

        connection.commit()

    print(f"JSON import done: {inserted} inserted, {overwritten} overwritten, {skipped} skipped.")


def display_contacts(contact_list):
    if not contact_list:
        print("  (no contacts)")
        return
    for contact in contact_list:
        cid      = contact[0]
        name     = contact[1]
        phone    = contact[2]
        email    = contact[3] if len(contact) > 3 else ""
        birthday = contact[4] if len(contact) > 4 else ""
        group    = contact[5] if len(contact) > 5 else ""
        print(f"  [{cid}] {name} - {phone} | {email or '-'} | {birthday or '-'} | {group or '-'}")


def main():
    create_tables()

    while True:
        print("\n--- PhoneBook ---")
        print("1.  Show all contacts")
        print("2.  Add contact (console)")
        print("3.  Import contacts from CSV")
        print("4.  Search contacts")
        print("5.  Update phone by name")
        print("6.  Update name by phone")
        print("7.  Delete contact by name or phone")
        print("8.  Delete contact by phone (confirm)")
        print("9.  Paginated view (next/prev)")
        print("10. Insert many contacts")
        print("11. Filter by group")
        print("12. Search by email")
        print("13. Add phone number to contact")
        print("14. Move contact to group")
        print("15. Export contacts to JSON")
        print("16. Import contacts from JSON")
        print("0.  Exit")

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
            name      = input("Enter name: ")
            new_phone = input("Enter new phone: ")
            update_contact_phone(name, new_phone)
        elif choice == "6":
            phone    = input("Enter phone: ")
            new_name = input("Enter new name: ")
            update_contact_name(phone, new_name)
        elif choice == "7":
            identifier = input("Enter name or phone: ")
            delete_contact(identifier)
        elif choice == "8":
            delete_contact_from_console()
        elif choice == "9":
            browse_contacts_paginated()
        elif choice == "10":
            n    = int(input("How many contacts: "))
            data = []
            for _ in range(n):
                name  = input("Name: ")
                phone = input("Phone: ")
                data.append((name, phone))
            insert_many_contacts(data)
        elif choice == "11":
            display_contacts(filter_by_group())
        elif choice == "12":
            display_contacts(search_by_email())
        elif choice == "13":
            add_phone_to_contact()
        elif choice == "14":
            move_contact_to_group()
        elif choice == "15":
            file_path = input("Output file path [contacts.json]: ").strip() or "contacts.json"
            export_to_json(file_path)
        elif choice == "16":
            file_path = input("Input file path [contacts.json]: ").strip() or "contacts.json"
            import_from_json(file_path)
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please try again.")

    connection.close()
    print("Thank you! Goodbye!")


if __name__ == "__main__":
    main()
