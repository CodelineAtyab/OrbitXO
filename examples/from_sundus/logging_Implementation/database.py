
import logging
import sqlite3
from pathlib import Path
from datetime import datetime

logger = logging.getLogger("database")
DB_PATH = Path(__file__).resolve().parent / "data.sqlite"

def _ensure_schema(conn: sqlite3.Connection):
    conn.execute(
        """CREATE TABLE IF NOT EXISTS travel_times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL,
                minutes INTEGER NOT NULL
            )"""
    )
    conn.commit()

def store_travel_time(minutes: int) -> None:
    logger.info("Connecting to database")
    conn = sqlite3.connect(DB_PATH)
    try:
        _ensure_schema(conn)
        logger.debug("Inserting record into travel_times: %s minutes", minutes)
        conn.execute(
            "INSERT INTO travel_times (created_at, minutes) VALUES (?, ?)",
            (datetime.utcnow().isoformat(timespec="seconds") + "Z", minutes),
        )
        conn.commit()
        logger.info("Storing new travel time record: %s minutes", minutes)
    except Exception:
        logger.exception("Failed to store travel time")
        raise
    finally:
        conn.close()
        logger.debug("Database connection closed")
