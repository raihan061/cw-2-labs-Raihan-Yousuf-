import bcrypt
import sqlite3
from pathlib import Path

from app.data.db import connect_database, DATA_DIR
from app.data.users import get_user_by_username, insert_user
from app.data.schema import create_users_table


def register_user(username, password, role='user'):
    """Register a new user with password hashing."""
    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    # Insert into DB
    insert_user(username, password_hash, role)

    return True, f"User '{username}' registered successfully."


def login_user(username, password):
    """Authenticate a user."""
    user = get_user_by_username(username)
    if not user:
        return False, "User not found."

    stored_hash = user[2]  # password_hash column

    if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
        return True, "Login successful!"

    return False, "Incorrect password."


def migrate_users_from_file(filepath=DATA_DIR / "users.txt"):
    """
    Migrate Week 7 users from users.txt → SQLite database.
    """
    if not filepath.exists():
        print(f"No users.txt file found at {filepath}")
        return 0

    conn = connect_database()
    cursor = conn.cursor()
    migrated_count = 0

    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split(",")
            if len(parts) >= 2:
                username = parts[0]
                password_hash = parts[1]

                try:
                    cursor.execute(
                        """
                        INSERT OR IGNORE INTO users
                        (username, password_hash, role)
                        VALUES (?, ?, ?)
                        """,
                        (username, password_hash, "user")
                    )

                    if cursor.rowcount > 0:
                        migrated_count += 1

                except sqlite3.Error as e:
                    print(f"Error migrating user '{username}': {e}")

    conn.commit()
    conn.close()

    print(f"Migrated {migrated_count} users from users.txt")
    return migrated_count
]