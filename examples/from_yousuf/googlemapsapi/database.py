import os
import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any, Union

DEFAULT_DB_PATH = os.path.join(os.path.dirname(__file__), "routes.sqlite3")

def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
	"""Return a sqlite3 connection with a dict-like row factory."""
	if db_path is None:
		db_path = DEFAULT_DB_PATH
	os.makedirs(os.path.dirname(db_path), exist_ok=True)
	conn = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
	conn.row_factory = sqlite3.Row
	return conn

def init_db(db_path: Optional[str] = None) -> None:
	"""Create the routes table if it doesn't exist."""
	if db_path is None:
		db_path = DEFAULT_DB_PATH
	conn = get_connection(db_path)
	try:
		cur = conn.cursor()
		cur.execute(
			"""
			CREATE TABLE IF NOT EXISTS routes (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				origin TEXT NOT NULL,
				destination TEXT NOT NULL,
				duration_text TEXT,
				duration_value REAL,
				distance_text TEXT,
				distance_value REAL,
				created_at TEXT NOT NULL
			)
			"""
		)
		conn.commit()
	finally:
		conn.close()

def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
	"""Convert sqlite3.Row to plain dict."""
	return {k: row[k] for k in row.keys()}

def insert_route(
	origin: str,
	destination: str,
	duration_text: Optional[str] = None,
	duration_value: Optional[Union[int, float]] = None,
	distance_text: Optional[str] = None,
	distance_value: Optional[Union[int, float]] = None,
	created_at: Optional[str] = None,
	db_path: Optional[str] = None,
) -> int:
	"""Insert a route record and return the inserted row id."""
	if db_path is None:
		db_path = DEFAULT_DB_PATH
	init_db(db_path)
	if created_at is None:
		created_at = datetime.utcnow().isoformat()
	conn = get_connection(db_path)
	try:
		cur = conn.cursor()
		cur.execute(
			"""
			INSERT INTO routes
				(origin, destination, duration_text, duration_value, distance_text, distance_value, created_at)
			VALUES (?, ?, ?, ?, ?, ?, ?)
			""",
			(
				origin,
				destination,
				duration_text,
				float(duration_value) if duration_value is not None else None,
				distance_text,
				float(distance_value) if distance_value is not None else None,
				created_at,
			),
		)
		conn.commit()
		return cur.lastrowid
	finally:
		conn.close()

def fetch_routes(limit: int = 100, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
	"""Fetch recent routes (most recent first)."""
	if db_path is None:
		db_path = DEFAULT_DB_PATH
	init_db(db_path)
	conn = get_connection(db_path)
	try:
		cur = conn.cursor()
		cur.execute("SELECT * FROM routes ORDER BY id DESC LIMIT ?", (limit,))
		rows = cur.fetchall()
		return [_row_to_dict(r) for r in rows]
	finally:
		conn.close()

def fetch_latest(db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
	"""Return the most recent route or None if none exists."""
	results = fetch_routes(limit=1, db_path=db_path)
	return results[0] if results else None

def clear_routes(db_path: Optional[str] = None) -> None:
	"""Delete all records from routes (useful for tests)."""
	if db_path is None:
		db_path = DEFAULT_DB_PATH
	init_db(db_path)
	conn = get_connection(db_path)
	try:
		cur = conn.cursor()
		cur.execute("DELETE FROM routes")
		conn.commit()
	finally:
		conn.close()
