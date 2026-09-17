from werkzeug.security import (
    generate_password_hash,
    check_password_hash,
)

from database.db import get_connection
from utils.validators import validate_username, validate_password


def hash_password(password):
    return generate_password_hash(password)


def validate_registration(username, password):
    username_valid, username_error = validate_username(username)

    if not username_valid:
        return False, username_error

    password_valid, password_error = validate_password(password)

    if not password_valid:
        return False, password_error

    return True, ""


def username_exists(username):
    connection = get_connection()

    try:
        row = connection.execute(
            "SELECT id FROM users WHERE username = ?",
            (username,),
        ).fetchone()

        return row is not None

    finally:
        connection.close()


def create_user(username, password):
    password_hash = hash_password(password)

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO users (username, password_hash, role)
            VALUES (?, ?, 'PLAYER')
            """,
            (username, password_hash),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()

def get_user_by_username(username):
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT id, username, password_hash, role, created_at
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        return row

    finally:
        connection.close()


def authenticate_user(username, password):
    user = get_user_by_username(username)

    if user is None:
        return None

    if not check_password_hash(user["password_hash"], password):
        return None

    return user