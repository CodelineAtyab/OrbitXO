import os
import mysql.connector
import json
import datetime

DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', 3306))
DB_USER = os.getenv('DB_USER', 'user')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'logsdb')

conn = None


def init_db():
    global conn
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
    )
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.database = DB_NAME
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            input_str VARCHAR(1024) NOT NULL,
            result JSON,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    cursor.close()


def save_interaction(input_str: str, result: list):
    if conn is None:
        init_db()
    cursor = conn.cursor()
    query = "INSERT INTO history (input_str, result, timestamp) VALUES (%s, %s, %s)"
    cursor.execute(query, (input_str, json.dumps(result), datetime.datetime.utcnow()))
    conn.commit()
    cursor.close()


def close_db():
    if conn is not None:
        conn.close()
