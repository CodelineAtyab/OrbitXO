import sqlite3
from typing import List, Tuple

DB_NAME = "history.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input TEXT NOT NULL,
            output TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def insert_history(input_str: str, output: List[int]):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO history (input, output) VALUES (?, ?)", (input_str, str(output)))
    conn.commit()
    conn.close()

def fetch_history() -> List[Tuple[int, str, str]]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, input, output FROM history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
