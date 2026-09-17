from werkzeug.security import generate_password_hash

from database.db import get_connection


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin1$"


def create_admin():
    connection = get_connection()

    try:
        existing_admin = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (ADMIN_USERNAME,),
        ).fetchone()

        if existing_admin:
            print("Admin user already exists.")
            return

        password_hash = generate_password_hash(ADMIN_PASSWORD)

        connection.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, 'ADMIN')
            """,
            (ADMIN_USERNAME, password_hash),
        )

        connection.commit()

        print("Admin user created successfully.")

    finally:
        connection.close()


if __name__ == "__main__":
    create_admin()