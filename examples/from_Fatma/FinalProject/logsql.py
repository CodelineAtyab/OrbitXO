import mysql.connector
from mysql.connector import Error
import datetime
import json
from contextlib import contextmanager
from log_config import logger


DB_CONFIG = {
    'host': 'db',
    'user': 'user',
    'password': 'password',
    'database': 'measurements_db'
}

@contextmanager
def db_connection():
    """Database connection context manager."""
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        yield conn
    except Error as e:
        logger.error(f"Database connection error: {e}")
        yield None
    finally:
        if conn and conn.is_connected():
            conn.close()

def log_request_response(input_str: str, output_data: dict):
    """Logs a request and its corresponding response to the MySQL database."""
    timestamp = datetime.datetime.now().isoformat()
    output_str = json.dumps(output_data)
    query = "INSERT INTO requests_log (timestamp, input_string, output_data) VALUES (%s, %s, %s)"
    
    with db_connection() as conn:
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, (timestamp, input_str, output_str))
                    conn.commit()
            except Error as e:
                logger.error(f"Error logging request to MySQL: {e}")