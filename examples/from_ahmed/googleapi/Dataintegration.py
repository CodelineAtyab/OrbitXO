import sqlite3
from datetime import datetime, timedelta
import threading
import time

DB_FILE = "travel_times.db"

# Database setup
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS travel_times (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            travel_time INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Record a travel time estimate
def record_travel_time(source, destination, travel_time):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO travel_times (timestamp, source, destination, travel_time)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, source, destination, travel_time))
    conn.commit()
    print(f"[INFO] Recorded travel time: {travel_time} minutes ({source} -> {destination}) at {timestamp}")
    conn.close()

# Retrieve historical data for a given day
def get_historical_data(source, destination, date_str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, travel_time FROM travel_times
        WHERE source = ? AND destination = ? AND date(timestamp) = ?
        ORDER BY timestamp ASC
    ''', (source, destination, date_str))
    rows = c.fetchall()
    conn.close()
    print(f"Date: {date_str}")
    for row in rows:
        time_part = row[0].split(' ')[1]
        print(f"{time_part} - {row[1]} minutes")
    return rows

def schedule_travel_time_recording(source, destination, get_travel_time_func):
    def job():
        while True:
            travel_time = get_travel_time_func(source, destination)
            record_travel_time(source, destination, travel_time)
            time.sleep(900)  # 15 minutes
    thread = threading.Thread(target=job, daemon=True)
    thread.start()

def example_get_travel_time(source, destination):
    
    import random
    return random.randint(20, 40)

if __name__ == "__main__":
    init_db()

    record_travel_time("home", "work", example_get_travel_time("home", "work"))
    get_historical_data("home", "work", datetime.now().strftime("%Y-%m-%d"))
