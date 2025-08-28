"""
Initialize SQLite database for travel time tracking.
"""
import sqlite3
import os
import sys

def initialize_database():
    """Initialize SQLite database from the SQL script."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "travel_time.db")
    sql_script_path = os.path.join(base_dir, "database.sql")
    
    print(f"[INFO] Initializing SQLite database at {db_path}")
    
    # Read SQL script
    try:
        with open(sql_script_path, 'r') as f:
            sql_script = f.read()
    except FileNotFoundError:
        print(f"[ERROR] SQL script not found at {sql_script_path}")
        return False
    
    # Connect to database and execute script
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        # Execute each statement in the script
        cursor.executescript(sql_script)
        
        connection.commit()
        connection.close()
        
        print(f"[INFO] Database initialized successfully at {db_path}")
        return True
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to initialize database: {e}")
        return False

if __name__ == "__main__":
    if initialize_database():
        sys.exit(0)
    else:
        sys.exit(1)
