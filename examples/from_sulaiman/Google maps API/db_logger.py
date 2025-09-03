import mysql.connector
from mysql.connector import Error
import logging
import os
import time
import schedule
from datetime import datetime
import json
from distance_matrix import get_distance_matrix

# Configure basic logging to a file
logging.basicConfig(
    filename='api2_logger.logs',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': 'localhost',  # Change as needed
    'database': 'travel_time_db',
    'user': 'your_username',  # Change this
    'password': 'your_password'  # Change this
}

def create_db_connection():
    """Create a connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logger.info(f"Connected to MySQL database: {DB_CONFIG['database']}")
            return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL database: {e}")
        return None

def setup_database():
    """Create the necessary tables if they don't exist"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            # Create travel_time_logs table
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS travel_time_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                origin VARCHAR(255) NOT NULL,
                destination VARCHAR(255) NOT NULL,
                distance_text VARCHAR(50),
                distance_value INT,
                duration_text VARCHAR(50),
                duration_value INT,
                status VARCHAR(50) NOT NULL
            )
            ''')
            
            # Create api_logs table for general logging
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id INT AUTO_INCREMENT PRIMARY KEY,
                timestamp DATETIME NOT NULL,
                log_level VARCHAR(20) NOT NULL,
                message TEXT NOT NULL,
                source VARCHAR(255)
            )
            ''')
            
            connection.commit()
            logger.info("Database tables created successfully")
        except Error as e:
            logger.error(f"Error setting up database tables: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def log_to_database(level, message, source="db_logger"):
    """Log a message to the database"""
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO api_logs (timestamp, log_level, message, source) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (datetime.now(), level, message, source))
            connection.commit()
        except Error as e:
            logger.error(f"Error logging to database: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def record_travel_time(origins, destinations, api_key=None):
    """Record travel time estimates in the database"""
    connection = create_db_connection()
    if not connection:
        logger.error("Failed to connect to database for recording travel time")
        return
    
    try:
        # Get distance matrix data
        logger.info(f"Requesting distance matrix from {origins} to {destinations}")
        result = get_distance_matrix(origins, destinations, api_key)
        
        # Log to database
        cursor = connection.cursor()
        
        if result.get("status") == "OK":
            for i, origin in enumerate(result["origin_addresses"]):
                for j, destination in enumerate(result["destination_addresses"]):
                    element = result["rows"][i]["elements"][j]
                    
                    # Prepare data for insertion
                    status = element.get("status", "UNKNOWN")
                    distance_text = element.get("distance", {}).get("text", None) if status == "OK" else None
                    distance_value = element.get("distance", {}).get("value", None) if status == "OK" else None
                    duration_text = element.get("duration", {}).get("text", None) if status == "OK" else None
                    duration_value = element.get("duration", {}).get("value", None) if status == "OK" else None
                    
                    # Insert into database
                    query = """
                    INSERT INTO travel_time_logs 
                    (timestamp, origin, destination, distance_text, distance_value, duration_text, duration_value, status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, (
                        datetime.now(),
                        origin,
                        destination,
                        distance_text,
                        distance_value,
                        duration_text,
                        duration_value,
                        status
                    ))
                    
                    # Log message
                    if status == "OK":
                        log_msg = f"Travel time from {origin} to {destination}: {duration_text}, Distance: {distance_text}"
                        logger.info(log_msg)
                        log_to_database("INFO", log_msg)
                    else:
                        log_msg = f"Failed to get travel time from {origin} to {destination}: {status}"
                        logger.error(log_msg)
                        log_to_database("ERROR", log_msg)
            
            connection.commit()
            logger.info("Travel time data recorded successfully")
        else:
            error_msg = f"Distance matrix request failed: {result.get('error_message', 'Unknown error')}"
            logger.error(error_msg)
            log_to_database("ERROR", error_msg)
            
    except Exception as e:
        logger.error(f"Exception occurred while recording travel time: {str(e)}")
        log_to_database("ERROR", f"Exception in record_travel_time: {str(e)}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_historical_data(origin=None, destination=None, start_time=None, end_time=None, limit=100):
    """
    Retrieve historical travel time data from database
    
    Args:
        origin (str): Filter by origin location
        destination (str): Filter by destination location
        start_time (datetime): Filter by start time
        end_time (datetime): Filter by end time
        limit (int): Maximum number of records to return
        
    Returns:
        list: List of travel time records
    """
    connection = create_db_connection()
    if not connection:
        logger.error("Failed to connect to database for retrieving historical data")
        return []
    
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Build query with optional filters
        query = "SELECT * FROM travel_time_logs WHERE 1=1"
        params = []
        
        if origin:
            query += " AND origin = %s"
            params.append(origin)
            
        if destination:
            query += " AND destination = %s"
            params.append(destination)
            
        if start_time:
            query += " AND timestamp >= %s"
            params.append(start_time)
            
        if end_time:
            query += " AND timestamp <= %s"
            params.append(end_time)
        
        query += " ORDER BY timestamp DESC LIMIT %s"
        params.append(limit)
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        logger.info(f"Retrieved {len(results)} historical travel time records")
        
        return results
        
    except Error as e:
        logger.error(f"Error retrieving historical data: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def record_scheduled_travel_times():
    """Function to be scheduled to record travel times every 15 minutes"""
    try:
        # Get API key from environment variable
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        
        # Example usage - you can modify these locations as needed
        origins = ["Seattle, WA"]
        destinations = ["San Francisco, CA", "Portland, OR"]
        
        # Record travel times
        record_travel_time(origins, destinations, api_key)
        
    except Exception as e:
        logger.error(f"Error in scheduled travel time recording: {str(e)}")
        log_to_database("ERROR", f"Scheduled task error: {str(e)}")

def analyze_travel_pattern(origin, destination, days=7):
    """
    Analyze travel time patterns between specific origin and destination
    
    Args:
        origin (str): Origin location
        destination (str): Destination location
        days (int): Number of days to analyze
        
    Returns:
        dict: Analysis results
    """
    connection = create_db_connection()
    if not connection:
        return {"error": "Database connection failed"}
        
    try:
        cursor = connection.cursor(dictionary=True)
        
        # Get average travel times by hour of day
        query = """
        SELECT 
            HOUR(timestamp) as hour_of_day,
            AVG(duration_value) as avg_duration_seconds,
            MIN(duration_value) as min_duration_seconds,
            MAX(duration_value) as max_duration_seconds,
            COUNT(*) as sample_count
        FROM travel_time_logs
        WHERE origin = %s 
            AND destination = %s
            AND timestamp >= DATE_SUB(NOW(), INTERVAL %s DAY)
            AND status = 'OK'
        GROUP BY HOUR(timestamp)
        ORDER BY hour_of_day
        """
        
        cursor.execute(query, (origin, destination, days))
        hourly_patterns = cursor.fetchall()
        
        return {
            "origin": origin,
            "destination": destination,
            "analysis_period_days": days,
            "hourly_patterns": hourly_patterns
        }
    
    except Error as e:
        logger.error(f"Error analyzing travel patterns: {e}")
        return {"error": str(e)}
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def start_scheduler():
    """Start the scheduler for periodic travel time recording"""
    # Schedule travel time recording every 15 minutes
    schedule.every(15).minutes.do(record_scheduled_travel_times)
    
    logger.info("Travel time scheduler started - recording every 15 minutes")
    log_to_database("INFO", "Travel time scheduler started")
    
    # Run the scheduler loop
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check scheduler every minute

if __name__ == "__main__":
    # Setup database tables
    setup_database()
    
    # Log startup
    startup_msg = "Database logger started"
    logger.info(startup_msg)
    log_to_database("INFO", startup_msg)
    
    # Record initial travel times
    try:
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        origins = ["Seattle, WA"]
        destinations = ["San Francisco, CA", "Portland, OR"]
        record_travel_time(origins, destinations, api_key)
    except Exception as e:
        logger.error(f"Error during initial travel time recording: {str(e)}")
    
    # Start the scheduler
    start_scheduler()
