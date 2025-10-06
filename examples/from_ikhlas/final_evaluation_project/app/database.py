from pathlib import Path
import sqlite3

# Ensure the directory exists
DB_DIR = Path("/app/data")
DB_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = Path("/app/data/db.sqlite3")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
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
