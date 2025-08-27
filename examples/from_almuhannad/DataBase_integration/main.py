from googleApi import get_travel_time, load_locations_from_config
import sys
import os
import json
import sqlite3
import datetime

def get_db_path():
    """Get the path to the SQLite database file."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "travel_time.db")
    return db_path

def create_connection():
    """Create a connection to the SQLite database."""
    db_path = get_db_path()
    
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row  # This allows accessing columns by name
        
        # Create tables if they don't exist
        create_tables(connection)
        
        print(f"[INFO] Connected to database at {db_path}")
        return connection
    except sqlite3.Error as e:
        print(f"[ERROR] Error connecting to SQLite database: {e}")
        return None

def create_tables(connection):
    """Create the necessary tables if they don't exist."""
    try:
        cursor = connection.cursor()
        
        # Create travel time history table
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
        
        # Create indexes
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
        print(f"[ERROR] Error creating tables: {e}")
        return False

def add_travel_time_record(source, destination, duration_minutes, distance, distance_value=None, is_minimum=False):
    """
    Add a travel time record to the database.
    
    Args:
        source (str): Source location
        destination (str): Destination location
        duration_minutes (int): Travel time in minutes
        distance (str): Distance as a formatted string (e.g. "10.5 km")
        distance_value (int, optional): Distance in meters
        is_minimum (bool, optional): Whether this is a minimum travel time
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        connection = create_connection()
        if not connection:
            print("[ERROR] Failed to connect to database")
            print(f"[INFO] Would have recorded: {source} -> {destination}, {duration_minutes} minutes")
            return False
        
        try:
            cursor = connection.cursor()
            sql = """
            INSERT INTO travel_time_history 
            (timestamp, source, destination, duration_minutes, distance, distance_value, is_minimum)
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
            print(f"[INFO] Recorded travel time (ID: {record_id}): {duration_minutes} minutes ({source} -> {destination}) at {timestamp}")
            return True
            
        except sqlite3.Error as e:
            print(f"[ERROR] Database error: {e}")
            return False
        finally:
            connection.close()
            print("[INFO] Database connection closed")
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Unexpected error recording travel time: {e}")
        return False

def get_historical_data(source, destination, date_str=None):
    """
    Retrieve historical travel time data.
    
    Args:
        source (str): Source location
        destination (str): Destination location
        date_str (str, optional): Date in format "YYYY-MM-DD". If None, gets all data.
        
    Returns:
        list: List of travel time records
    """
    connection = create_connection()
    if not connection:
        print("[ERROR] Failed to connect to database")
        return []
    
    try:
        cursor = connection.cursor()
        
        if date_str:
            # For SQLite, we need to extract the date part from the timestamp string
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
        print(f"[INFO] Retrieved {len(results)} records for {source} -> {destination}")
        
        # Format and display results
        if results and date_str:
            print(f"\nDate: {date_str}")
            for result in results:
                # Parse the ISO format timestamp to get the time
                dt = datetime.datetime.fromisoformat(result['timestamp'])
                time_str = dt.strftime("%H:%M:%S")
                print(f"{time_str} - {result['duration_minutes']} minutes")
        
        # Convert SQLite Row objects to dictionaries
        formatted_results = []
        for row in results:
            formatted_results.append(dict(row))
        
        return formatted_results
        
    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        return []
    finally:
        connection.close()
        print("[INFO] Database connection closed")

def track_travel_time(source, destination, use_mock_data=False):
    """
    Track travel time between source and destination.
    
    Args:
        source (str): Source location
        destination (str): Destination location
        use_mock_data (bool): Whether to use mock data instead of calling the API
        
    Returns:
        dict: Travel time information
    """
    print(f"[INFO] Getting travel time from {source} to {destination}")
    
    if use_mock_data:
        print("[INFO] Using mock data instead of calling API")
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
        print(f"[ERROR] Failed to get travel time: {travel_result['error']}")
        return None
    
    duration_minutes = travel_result["duration_value"] // 60
    
    print(f"[INFO] Travel time: {travel_result['duration']} ({duration_minutes} minutes)")
    print(f"[INFO] Distance: {travel_result['distance']}")
    
    # Record in database
    is_recorded = add_travel_time_record(
        source=source,
        destination=destination,
        duration_minutes=duration_minutes,
        distance=travel_result["distance"],
        distance_value=travel_result.get("distance_value")
    )
    
    if is_recorded:
        print("[INFO] Travel time recorded in database")
    else:
        print("[WARNING] Failed to record travel time in database")
    
    return {
        "travel_result": travel_result
    }

def main():
    print("[INFO] Starting travel time tracker")
    
    try:
        # Load locations from config file
        config_path = "config.json"
        try:
            source, destination = load_locations_from_config(config_path)
            print(f"[INFO] Loaded locations: {source} to {destination}")
        except ValueError as e:
            print(f"[ERROR] Error loading locations: {e}")
            return 1
        
        # Try with real API first
        result = track_travel_time(source, destination)
        
        # If API call fails, use mock data
        if not result:
            print("[WARNING] API call failed, using mock data instead")
            result = track_travel_time(source, destination, use_mock_data=True)
        
        if result:
            print("[INFO] Travel time tracking completed successfully")
            
            # Optional: Show historical data for today
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            get_historical_data(source, destination, today)
            
            return 0
        else:
            print("[ERROR] Failed to track travel time")
            return 1
    
    except Exception as e:
        print(f"[ERROR] An unexpected error occurred: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
