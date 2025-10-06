import mysql.connector
from mysql.connector import Error
import datetime
import json
import time
import os

# --- IMPORTANT ---
# These credentials match the docker-compose.yml file.
# The 'host' is the name of the database service in Docker Compose.
DB_CONFIG = {
    'host': 'db',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'api_log_db'
}

def log_request_response(input_str: str, output_data: dict):
    """Logs a request and its corresponding response to the MySQL database."""
    conn = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        timestamp = datetime.datetime.now().isoformat()
        output_str = json.dumps(output_data)
        
        query = "INSERT INTO requests_log (timestamp, input_string, output_data) VALUES (%s, %s, %s)"
        cursor.execute(query, (timestamp, input_str, output_str))
        
        conn.commit()
    except Error as e:
        print(f"Error logging request to MySQL: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()