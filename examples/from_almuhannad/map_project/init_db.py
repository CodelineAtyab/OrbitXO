import sqlite3
import os
import sys

def initialize_database():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "travel_time.db")
    sql_script_path = os.path.join(base_dir, "database.sql")
    
    try:
        with open(sql_script_path, 'r') as f:
            sql_script = f.read()
    except FileNotFoundError:
        return False
    
    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        
        cursor.executescript(sql_script)
        
        connection.commit()
        connection.close()
        
        return True
    except sqlite3.Error as e:
        return False

if __name__ == "__main__":
    if initialize_database():
        sys.exit(0)
    else:
        sys.exit(1)
