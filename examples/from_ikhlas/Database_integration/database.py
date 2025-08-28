import sqlite3

connection=sqlite3.connect("traffic.db")
cursor=connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS travel_times (
    I INTEGER PRIMARY KEY AUTOINCREMENT,
    Timestamp TEXT NOT NULL,
    Source TEXT NOT NULL,
    Destination TEXT NOT NULL,
    Duration_minutes REAL,
    Distance_km REAL
)
""")

connection.commit()
connection.close()

print("[INFO] SQLite database initialized: traffic.db")
