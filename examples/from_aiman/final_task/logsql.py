import mysql.connector
from mysql.connector import Error
import datetime
import json
import os

class DatabaseLogger:
    """Handles logging of requests and responses to a MySQL database."""

    def __init__(self):
        """Initializes the database logger with connection details from environment variables."""
        self.db_config = {
            'host': os.getenv('MYSQL_HOST', 'db'),
            'user': os.getenv('MYSQL_USER', 'your_username'),
            'password': os.getenv('MYSQL_PASSWORD', 'your_password'),
            'database': os.getenv('MYSQL_DATABASE', 'api_log_db')
        }

    def log_interaction(self, request_payload: str, response_payload: dict):
        """Logs a single request and response interaction to the database."""
        query = "INSERT INTO requests_log (timestamp, input_string, output_data) VALUES (%s, %s, %s)"
        timestamp = datetime.datetime.now().isoformat()
        response_json = json.dumps(response_payload)
        
        try:
            with mysql.connector.connect(**self.db_config) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, (timestamp, request_payload, response_json))
                    connection.commit()
        except Error as e:
           
            print(f"Error: Failed to log request to MySQL. Details: {e}")


db_logger = DatabaseLogger()