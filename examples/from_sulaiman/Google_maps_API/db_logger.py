import sqlite3
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
DB_PATH = 'travel_time.db'  # SQLite database file path

def create_db_connection():
    """Create a connection to the SQLite database"""
    try:
        connection = sqlite3.connect(DB_PATH)
        logger.info(f"Connected to SQLite database: {DB_PATH}")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to SQLite database: {e}")
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                origin TEXT NOT NULL,
                destination TEXT NOT NULL,
                distance_text TEXT,
                distance_value INTEGER,
                duration_text TEXT,
                duration_value INTEGER,
                status TEXT NOT NULL
            )
            ''')
            
            # Create api_logs table for general logging
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME NOT NULL,
                log_level TEXT NOT NULL,
                message TEXT NOT NULL,
                source TEXT
            )
            ''')
            
            # Commit changes to create tables
            connection.commit()
            
            # Verify tables were created
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            if 'travel_time_logs' in table_names and 'api_logs' in table_names:
                logger.info(f"Database tables created successfully: {table_names}")
                print(f"✓ Database tables created successfully: {table_names}")
            else:
                logger.error(f"Failed to create all required tables. Found: {table_names}")
                print(f"✗ Failed to create all required tables. Found: {table_names}")
                
        except Exception as e:
            logger.error(f"Error setting up database tables: {e}")
            print(f"✗ Error setting up database tables: {e}")
        finally:
            cursor.close()
            connection.close()

def log_to_database(level, message, source="db_logger"):
    """Log a message to the database"""
    # Make sure the table exists
    setup_database()
    
    connection = create_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO api_logs (timestamp, log_level, message, source) 
            VALUES (?, ?, ?, ?)
            """
            # Format datetime for SQLite
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(query, (timestamp, level, message, source))
            connection.commit()
            return True
        except Exception as e:
            logger.error(f"Error logging to database: {e}")
            return False
        finally:
            cursor.close()
            connection.close()

def record_travel_time(origins, destinations, api_key=None):
    """Record travel time estimates in the database"""
    # Check if database tables exist, create them if not
    setup_database()
    
    # Connect to database
    connection = create_db_connection()
    if not connection:
        logger.error("Failed to connect to database for recording travel time")
        print("✗ Failed to connect to database for recording travel time")
        return False
    
    try:
        # Get distance matrix data
        logger.info(f"Requesting distance matrix from {origins} to {destinations}")
        print(f"Requesting distance matrix from {origins} to {destinations}")
        result = get_distance_matrix(origins, destinations, api_key)
        
        # Log to database
        cursor = connection.cursor()
        records_added = 0
        
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
                    try:
                        query = """
                        INSERT INTO travel_time_logs 
                        (timestamp, origin, destination, distance_text, distance_value, duration_text, duration_value, status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """
                        cursor.execute(query, (
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Format timestamp for SQLite
                            origin,
                            destination,
                            distance_text,
                            distance_value,
                            duration_text,
                            duration_value,
                            status
                        ))
                        records_added += 1
                        
                        # Log message
                        if status == "OK":
                            log_msg = f"Travel time from {origin} to {destination}: {duration_text}, Distance: {distance_text}"
                            logger.info(log_msg)
                            
                            # Log to the api_logs table
                            try:
                                log_query = """
                                INSERT INTO api_logs (timestamp, log_level, message, source) 
                                VALUES (?, ?, ?, ?)
                                """
                                cursor.execute(log_query, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "INFO", log_msg, "record_travel_time"))
                            except Exception as e:
                                logger.error(f"Failed to log to api_logs table: {e}")
                        else:
                            log_msg = f"Failed to get travel time from {origin} to {destination}: {status}"
                            logger.error(log_msg)
                    except Exception as e:
                        logger.error(f"Error inserting record into database: {e}")
                        print(f"✗ Error inserting record into database: {e}")
            
            # Make sure to commit after all records are added
            connection.commit()
            
            if records_added > 0:
                logger.info(f"Travel time data recorded successfully ({records_added} records)")
                print(f"✓ Travel time data recorded successfully ({records_added} records)")
                
                # Verify the data was added
                cursor.execute("SELECT COUNT(*) FROM travel_time_logs")
                count = cursor.fetchone()[0]
                print(f"Total records in database: {count}")
                
                return True
            else:
                logger.warning("No travel time records were added to the database")
                print("⚠ No travel time records were added to the database")
                return False
        else:
            error_msg = f"Distance matrix request failed: {result.get('error_message', 'Unknown error')}"
            logger.error(error_msg)
            print(f"✗ {error_msg}")
            return False
            
    except Exception as e:
        logger.error(f"Exception occurred while recording travel time: {str(e)}")
        log_to_database("ERROR", f"Exception in record_travel_time: {str(e)}")
    finally:
        if connection:
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
        list: List of travel time records as dictionaries
    """
    # First check if tables exist
    setup_database()
    
    connection = create_db_connection()
    if not connection:
        logger.error("Failed to connect to database for retrieving historical data")
        print("✗ Failed to connect to database for retrieving historical data")
        return []
    
    try:
        # Configure SQLite connection to return dictionaries
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        # Check if table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='travel_time_logs'")
        if not cursor.fetchone():
            logger.error("travel_time_logs table does not exist")
            print("✗ travel_time_logs table does not exist")
            return []
        
        # Build query with optional filters
        query = "SELECT * FROM travel_time_logs WHERE 1=1"
        params = []
        
        if origin:
            query += " AND origin = ?"
            params.append(origin)
            
        if destination:
            query += " AND destination = ?"
            params.append(destination)
            
        if start_time:
            query += " AND timestamp >= ?"
            params.append(start_time)
            
        if end_time:
            query += " AND timestamp <= ?"
            params.append(end_time)
        
        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Convert SQLite Row objects to dictionaries for easier handling
        results = []
        for row in rows:
            results.append({key: row[key] for key in row.keys()})
        
        logger.info(f"Retrieved {len(results)} historical travel time records")
        print(f"Retrieved {len(results)} historical travel time records")
        
        # If no results, try checking total count in table
        if len(results) == 0:
            cursor.execute("SELECT COUNT(*) FROM travel_time_logs")
            count = cursor.fetchone()[0]
            print(f"Note: There are {count} total records in the travel_time_logs table")
            
            if count > 0 and (origin or destination):
                print(f"Check if your filters (origin='{origin}', destination='{destination}') match the data in the table")
                # Print a sample of what's in the table
                cursor.execute("SELECT origin, destination FROM travel_time_logs LIMIT 3")
                sample = cursor.fetchall()
                print(f"Sample data in table: {[dict(row) for row in sample]}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error retrieving historical data: {e}")
        print(f"✗ Error retrieving historical data: {e}")
        return []
    finally:
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
        # Configure SQLite connection to return dictionaries
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()
        
        # Get average travel times by hour of day
        query = """
        SELECT 
            CAST(strftime('%H', timestamp) AS INTEGER) as hour_of_day,
            AVG(duration_value) as avg_duration_seconds,
            MIN(duration_value) as min_duration_seconds,
            MAX(duration_value) as max_duration_seconds,
            COUNT(*) as sample_count
        FROM travel_time_logs
        WHERE origin = ? 
            AND destination = ?
            AND timestamp >= datetime('now', '-' || ? || ' days')
            AND status = 'OK'
        GROUP BY hour_of_day
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
    
    except Exception as e:
        logger.error(f"Error analyzing travel patterns: {e}")
        return {"error": str(e)}
    finally:
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
