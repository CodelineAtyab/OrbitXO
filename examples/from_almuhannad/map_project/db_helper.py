import os
import datetime
import mysql.connector
from dotenv import load_dotenv
from typing import Dict, Any, List, Optional

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

def create_connection():
    """Create a connection to the MySQL database"""
    try:
        config = get_db_config()
        connection = mysql.connector.connect(**config)
        return connection
    except mysql.connector.Error as e:
        print(f"Database connection error: {e}")
        return None

def add_travel_time_record(source, destination, duration_minutes, distance, distance_value=None, is_minimum=False):
    """Add a travel time record to the database"""
    try:
        connection = create_connection()
        if not connection:
            return False
        
        cursor = connection.cursor()
        sql = """
        INSERT INTO travel_time_history 
        (timestamp, source, destination, duration_minutes, distance, distance_value, is_minimum)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        timestamp = datetime.datetime.now()
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
        cursor.close()
        connection.close()
        
        return True
    except mysql.connector.Error as e:
        print(f"Database insert error: {e}")
        return False

def get_historical_data(source, destination, date_str=None):
    """Get historical travel time data from the database"""
    connection = create_connection()
    if not connection:
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        if date_str:
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
            start_date = date_obj.strftime("%Y-%m-%d 00:00:00")
            end_date = date_obj.strftime("%Y-%m-%d 23:59:59")
            
            sql = """
            SELECT * FROM travel_time_history 
            WHERE source = %s AND destination = %s AND timestamp BETWEEN %s AND %s
            ORDER BY timestamp DESC
            """
            cursor.execute(sql, (source, destination, start_date, end_date))
        else:
            sql = """
            SELECT * FROM travel_time_history 
            WHERE source = %s AND destination = %s
            ORDER BY timestamp DESC LIMIT 30
            """
            cursor.execute(sql, (source, destination))
        
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return results
    except mysql.connector.Error as e:
        print(f"Database query error: {e}")
        return []

def get_minimum_travel_time(source, destination):
    """Get the minimum travel time record for a route"""
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        sql = """
        SELECT * FROM travel_time_history 
        WHERE source = %s AND destination = %s
        ORDER BY duration_minutes ASC
        LIMIT 1
        """
        cursor.execute(sql, (source, destination))
        
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        return result
    except mysql.connector.Error as e:
        print(f"Database query error: {e}")
        return None
