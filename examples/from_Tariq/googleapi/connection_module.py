import os
import datetime
import logging
import mysql.connector
from mysql.connector import Error

_logger = logging.getLogger("db_connector")
_conn = None

def initialize_connection():
    global _conn
    try:
        # Get connection parameters from environment variables or use defaults
        host = os.environ.get('MYSQL_HOST', 'mysql')
        user = os.environ.get('MYSQL_USER', 'orbitxo')
        password = os.environ.get('MYSQL_PASSWORD', 'yourpassword')
        database = os.environ.get('MYSQL_DATABASE', 'traveltime')
        port = int(os.environ.get('MYSQL_PORT', '3306'))
        
        _conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            port=port
        )
        
        _logger.info(f"MySQL database connection initialized to {host}:{port}/{database}")
        return True
    except Error as e:
        _logger.error(f"Database connection failed: {e}")
        return False

def add_travel_time_record(source, destination, duration_minutes, distance=None, distance_value=None, is_minimum=False):
    global _conn
    
    if _conn is None or not _conn.is_connected():
        if not initialize_connection():
            return False
        
    try:
        cursor = _conn.cursor()
        
        query = """
        INSERT INTO travel_time_history 
        (timestamp, source, destination, duration_minutes, distance, distance_value, is_minimum)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        values = (
            datetime.datetime.now(),
            source,
            destination,
            duration_minutes,
            distance,
            distance_value,
            is_minimum
        )
        
        cursor.execute(query, values)
        _conn.commit()
        cursor.close()
            
        _logger.info(f"Added travel time record: {source} to {destination}, {duration_minutes} minutes")
        return True
        
    except Error as e:
        _logger.error(f"Failed to add travel time record: {e}")
        return False

def get_travel_time_history(source=None, destination=None, start_date=None, end_date=None, limit=100):
    global _conn
    
    if _conn is None or not _conn.is_connected():
        if not initialize_connection():
            return []
        
    try:
        cursor = _conn.cursor(dictionary=True)
        
        query = "SELECT * FROM travel_time_history WHERE 1=1"
        params = []
        
        if source:
            query += " AND source = %s"
            params.append(source)
        if destination:
            query += " AND destination = %s"
            params.append(destination)
        if start_date:
            query += " AND timestamp >= %s"
            params.append(start_date)
        if end_date:
            query += " AND timestamp <= %s"
            params.append(end_date)
            
        query += " ORDER BY timestamp DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        records = cursor.fetchall()
        cursor.close()
            
        _logger.info(f"Retrieved {len(records)} travel time records")
        return records
        
    except Error as e:
        _logger.error(f"Failed to retrieve travel time history: {e}")
        return []

def get_minimum_travel_times(source=None, destination=None):
    global _conn
    
    if _conn is None or not _conn.is_connected():
        if not initialize_connection():
            return []
        
    try:
        cursor = _conn.cursor(dictionary=True)
        
        query = """
        SELECT source, destination, MIN(duration_minutes) as min_duration
        FROM travel_time_history
        WHERE 1=1
        """
        
        params = []
        
        if source:
            query += " AND source = %s"
            params.append(source)
        if destination:
            query += " AND destination = %s"
            params.append(destination)
            
        query += " GROUP BY source, destination"
        
        cursor.execute(query, params)
        records = cursor.fetchall()
        cursor.close()
        
        _logger.info(f"Retrieved {len(records)} minimum travel time records")
        return records
        
    except Error as e:
        _logger.error(f"Failed to retrieve minimum travel times: {e}")
        return []

def get_db_connector():
    if _conn is None or not _conn.is_connected():
        if not initialize_connection():
            _logger.error("Failed to initialize database connection")
            return {
                "add_travel_time_record": lambda **kwargs: False,
                "get_travel_time_history": lambda **kwargs: [],
                "get_minimum_travel_times": lambda **kwargs: []
            }
    
    return {
        "add_travel_time_record": add_travel_time_record,
        "get_travel_time_history": get_travel_time_history,
        "get_minimum_travel_times": get_minimum_travel_times
    }