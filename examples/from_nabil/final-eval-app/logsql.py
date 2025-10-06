import mysql.connector
import json
from datetime import datetime
from typing import Any, Dict
import os
import time

def get_db_connection():
    """Get a connection to the MySQL database."""
    conn = None
    attempts = 0
    while attempts < 10 and conn is None:
        try:
            conn = mysql.connector.connect(
                host=os.environ.get("DB_HOST", "localhost"),
                user=os.environ.get("DB_USER", "user"),
                password=os.environ.get("DB_PASSWORD", "password"),
                database=os.environ.get("DB_NAME", "api_logs_db")
            )
        except mysql.connector.Error as err:
            print(f"Error connecting to database: {err}")
            time.sleep(5)
            attempts += 1
    return conn

def log_request_response(input_data: str, response_data: Dict[str, Any]) -> None:
    """
    Log the request input and response data to the database.
    
    Args:
        input_data: The input string that was processed
        response_data: The response data dictionary containing input_string and output
    """
    conn = get_db_connection()
    if conn is None:
        print("Could not establish database connection.")
        return
        
    try:
        cursor = conn.cursor()
        timestamp = datetime.now()
        query = 'INSERT INTO request_logs (timestamp, input_data, output_data) VALUES (%s, %s, %s)'
        cursor.execute(query, (timestamp, input_data, json.dumps(response_data)))
        conn.commit()
    except Exception as e:
        print(f"Error logging to database: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()