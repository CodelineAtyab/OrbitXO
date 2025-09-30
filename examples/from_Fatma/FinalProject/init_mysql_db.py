import mysql.connector
import os
import sys
import time
from dotenv import load_dotenv
# Load environment variables
load_dotenv()
def get_db_config():
    """Get MySQL database configuration from environment variables"""
    return {
        'host': os.environ.get('MYSQL_HOST', 'db'),
        'port': int(os.environ.get('MYSQL_PORT', 3306)),
        'user': os.environ.get('MYSQL_USER', 'mapuser'),
        'password': os.environ.get('MYSQL_PASSWORD', 'mappassword'),
        'database': os.environ.get('MYSQL_DATABASE', 'travel_times'),
    }
def wait_for_db():
    """Wait for database to be available"""
    config = get_db_config()
    max_retries = 30
    retry_interval = 2
    for i in range(max_retries):
        try:
            # Try to connect without database name first
            conn = mysql.connector.connect(
                host=config['host'],
                port=config['port'],
                user=config['user'],
                password=config['password']
            )
            conn.close()
            return True
        except mysql.connector.Error:
            print(f"Waiting for database to be ready... ({i+1}/{max_retries})")
            time.sleep(retry_interval)
    return False
def initialize_database():
    """Initialize the MySQL database with the schema"""
    if not wait_for_db():
        print("Database connection timed out")
        return False
    config = get_db_config()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sql_script_path = os.path.join(base_dir, "mysql_schema.sql")
    try:
        with open(sql_script_path, 'r') as f:
            sql_script = f.read()
    except FileNotFoundError:
        print(f"SQL script not found: {sql_script_path}")
        return False
    try:
        # First ensure the database exists
        conn = mysql.connector.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password']
        )
        cursor = conn.cursor()
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {config['database']}")
        conn.close()
        # Connect to the specific database
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        # Split and execute SQL statements
        statements = sql_script.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        conn.close()
        print("Database initialized successfully")
        return True
    except mysql.connector.Error as e:
        print(f"Database initialization error: {e}")
        return False
if __name__ == "__main__":
    if initialize_database():
        sys.exit(0)
    else:
        sys.exit(1)