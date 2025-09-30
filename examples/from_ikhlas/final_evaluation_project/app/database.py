import sqlite3
from pathlib import Path

DB_PATH = Path("./db.sqlite3")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_str TEXT NOT NULL,
            output_str TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
