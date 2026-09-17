import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "guess_the_word.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


WORDS = [
    "APPLE",
    "HOUSE",
    "TIGER",
    "PLANT",
    "CHAIR",
    "MOUSE",
    "WATER",
    "LIGHT",
    "WORLD",
    "STONE",
    "BREAD",
    "GREEN",
    "BLACK",
    "SMILE",
    "CLOUD",
    "RIVER",
    "HEART",
    "TRAIN",
    "MUSIC",
    "EARTH",
]


def initialize_database():
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            schema = schema_file.read()

        connection.executescript(schema)

        for word in WORDS:
            connection.execute(
                "INSERT OR IGNORE INTO words (word) VALUES (?)",
                (word,)
            )

        connection.commit()

        print("Database initialized successfully.")
        print(f"Inserted {len(WORDS)} seed words.")

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        connection.close()


if __name__ == "__main__":
    initialize_database()