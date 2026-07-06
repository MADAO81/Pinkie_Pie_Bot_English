# bot/scripts/create_recipe_db.py
"""
Script to create the recipe database.
Run once to initialize.

Author: MADAO81
Version: 2.0
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "data" / "recipes.db"


def init_db():
    """Creates the recipe table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            ingredients TEXT NOT NULL,
            instructions TEXT NOT NULL,
            category TEXT DEFAULT 'baking',
            source TEXT DEFAULT 'database'
        )
    """)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


if __name__ == "__main__":
    init_db()
