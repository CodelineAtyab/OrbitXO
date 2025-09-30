import mysql.connector
import os
import time
import logging
from typing import Optional, Any, Dict

logger = logging.getLogger(__name__)


def get_connection(retries: int = 6, delay: float = 2.0):
    """Return a MySQL connection, retrying a few times if the DB isn't ready yet."""
    host = os.getenv("DB_HOST", "db")
    port = int(os.getenv("DB_PORT", 3306))
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASS", "root")
    database = os.getenv("DB_NAME", "measurements")

    last_exc = None
    for attempt in range(1, retries + 1):
        try:
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                auth_plugin="mysql_native_password",
                connection_timeout=5,
            )
            return conn
        except mysql.connector.Error as e:
            last_exc = e
            logger.warning("DB connection attempt %d/%d failed: %s", attempt, retries, e)
            if attempt < retries:
                time.sleep(delay)
    # all attempts failed
    logger.error("DB connection failed after %d attempts: %s", retries, last_exc)
    raise last_exc


def _ensure_history_table(conn: Any):
    """Create a richer history table if it does not exist.

    The table stores request/response details in addition to the original
    input/result columns so the UI can show full interactions.
    """
    cursor = conn.cursor()
    try:
        # create if not exists (handles new DBs)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                input_str VARCHAR(2549),
                result_str VARCHAR(2549),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """
        )
        conn.commit()

        # ensure new columns exist on older schemas (init.sql may have only input_str/result_str)
        cursor.execute("SHOW COLUMNS FROM history")
        existing = {row[0] for row in cursor.fetchall()}  # column names

        needed = {
            "method": "VARCHAR(10)",
            "path": "VARCHAR(2048)",
            "query_string": "TEXT",
            "request_body": "TEXT",
            "response_body": "TEXT",
            "status_code": "INT",
            "input_str": "VARCHAR(2549)",
            "result_str": "VARCHAR(2549)",
        }

        for col, coltype in needed.items():
            if col not in existing:
                # add column allowing NULLs to avoid breaking existing data
                sql = f"ALTER TABLE history ADD COLUMN `{col}` {coltype} NULL"
                cursor.execute(sql)
        conn.commit()
    finally:
        cursor.close()


def save_history(
    input_str: Optional[str] = None,
    result: Optional[Any] = None,
    *,
    method: Optional[str] = None,
    path: Optional[str] = None,
    query_string: Optional[str] = None,
    request_body: Optional[str] = None,
    response_body: Optional[str] = None,
    status_code: Optional[int] = None,
):
    """Save one interaction into the history table.

    Accepts both the old (input_str, result) parameters and the newer
    request/response fields. Fields that are None will be stored as NULL.
    """
    conn = None
    cursor = None
    try:
        conn = get_connection()
        _ensure_history_table(conn)
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO history
                (method, path, query_string, request_body, response_body, status_code, input_str, result_str)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                method,
                path,
                query_string,
                request_body,
                response_body,
                status_code,
                # some DBs (init.sql) created input_str/result_str NOT NULL — coerce to empty string to avoid insert errors
                "" if input_str is None else input_str,
                "" if result is None else str(result),
            ),
        )
        conn.commit()
    except mysql.connector.Error as e:
        logger.exception("DB save_history error")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_history():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        _ensure_history_table(conn)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM history ORDER BY id DESC")
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as e:
        logger.exception("DB get_history error")
        raise
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
