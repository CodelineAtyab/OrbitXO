from googleApi import get_travel_time, load_locations_from_config
import sys
import os
import json
import sqlite3
import datetime

def get_db_path():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "travel_time.db")
    return db_path

def create_connection():
    db_path = get_db_path()
    
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        
        create_tables(connection)
        
        return connection
    except sqlite3.Error as e:
        return None

def create_tables(connection):
    try:
        cursor = connection.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS travel_time_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL,
            destination TEXT NOT NULL,
            duration_minutes INTEGER NOT NULL,
            distance TEXT,
            distance_value INTEGER,
            is_minimum BOOLEAN DEFAULT 0
        )
        ''')
        
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_source_dest 
        ON travel_time_history(source, destination)
        ''')
        
        cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_timestamp 
        ON travel_time_history(timestamp)
        ''')
        
        connection.commit()
        return True
    except sqlite3.Error as e:
        return False

def add_travel_time_record(source, destination, duration_minutes, distance, distance_value=None, is_minimum=False):
    try:
        connection = create_connection()
        if not connection:
            return False
        
        try:
            cursor = connection.cursor()
            sql = """
            INSERT INTO travel_time_history (timestamp, source, destination, duration_minutes, distance, distance_value, is_minimum)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            timestamp = datetime.datetime.now().isoformat()
            cursor.execute(sql, (
                timestamp,
                source,
                destination,
                duration_minutes,
                distance,
                distance_value,
                1 if is_minimum else 0
            ))
            
            connection.commit()
            record_id = cursor.lastrowid
            return True
            
        except sqlite3.Error as e:
            return False
        finally:
            connection.close()
    except Exception as e:
        return False

def get_historical_data(source, destination, date_str=None):
    connection = create_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor()
        
        if date_str:
            sql = """
            SELECT timestamp, duration_minutes, distance
            FROM travel_time_history
            WHERE source = ? AND destination = ? 
            AND substr(timestamp, 1, 10) = ?
            ORDER BY timestamp
            """
            cursor.execute(sql, (source, destination, date_str))
        else:
            sql = """
            SELECT timestamp, duration_minutes, distance
            FROM travel_time_history
            WHERE source = ? AND destination = ?
            ORDER BY timestamp DESC
            LIMIT 100
            """
            cursor.execute(sql, (source, destination))
            
        results = cursor.fetchall()
        
        formatted_results = []
        for row in results:
            formatted_results.append(dict(row))
        
        return formatted_results
        
    except sqlite3.Error as e:
        return []
    finally:
        connection.close()

def track_travel_time(source, destination, use_mock_data=False):
    if use_mock_data:
        travel_result = {
            "success": True,
            "source": source,
            "destination": destination,
            "distance": "1012.5 km",
            "distance_value": 1012500,
            "duration": "10 hours 30 min",
            "duration_value": 37800
        }
    else:
        travel_result = get_travel_time(source, destination)
    
    if not travel_result["success"]:
        return None
    
    duration_minutes = travel_result["duration_value"] // 60
    
    add_travel_time_record(
        source=source,
        destination=destination,
        duration_minutes=duration_minutes,
        distance=travel_result["distance"],
        distance_value=travel_result.get("distance_value")
    )
    
    return {
        "travel_result": travel_result
    }

def main():
    try:
        config_path = "config.json"
        try:
            source, destination = load_locations_from_config(config_path)
        except ValueError as e:
            return 1
        
        result = track_travel_time(source, destination)
        
        if not result:
            result = track_travel_time(source, destination, use_mock_data=True)
        
        if result:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            get_historical_data(source, destination, today)
            return 0
        else:
            return 1
    
    except Exception as e:
        return 1

if __name__ == "__main__":
    sys.exit(main())
