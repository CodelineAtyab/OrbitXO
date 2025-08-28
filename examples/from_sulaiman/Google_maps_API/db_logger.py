"""
Database Logger Module for Google Maps Route Tracking System

This module handles all database operations for the route tracking system,
including logging events and recording travel time data.
"""
import logging
import os
import time
import schedule
import subprocess
import json
from datetime import datetime
from distance_matrix import get_distance_matrix

# Import MySQL connector
try:
    import mysql.connector
    from mysql.connector import Error
except ImportError:
    logging.error("MySQL Connector package not installed. Please run 'pip install mysql-connector-python'")
    print("Error: MySQL Connector package not installed. Please run 'pip install mysql-connector-python'")

# Import Docker
try:
    import docker
except ImportError:
    logging.error("Docker SDK not installed. Please run 'pip install docker'")
    print("Error: Docker SDK not installed. Please run 'pip install docker'")

# Import database config
try:
    from db_config import get_db_config
    # Test if it works
    DB_CONFIG = get_db_config()
    logging.info("Successfully loaded database configuration")
except ImportError as e:
    logging.error(f"Failed to import db_config: {e}")
    print(f"Error: Failed to import db_config: {e}")
    # Define a fallback configuration
    DB_CONFIG = {
        'host': 'localhost',
        'port': 3306,
        'user': 'route_user',
        'password': 'route_password',
        'database': 'route_tracker'
    }

# Configure basic logging to a file
logging.basicConfig(
    filename='logs/database.log',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

def check_docker_running():
    """Check if Docker is running on the system"""
    try:
        client = docker.from_env()
        client.ping()
        logger.info("Docker is running")
        return True
    except Exception as e:
        logger.error(f"Docker is not running or not accessible: {e}")
        return False

def start_mysql_container():
    """Start the MySQL container if it's not running"""
    try:
        # Check if Docker is running
        if not check_docker_running():
            logger.error("Docker is not running. Cannot start MySQL container.")
            print("✗ Docker is not running. Please start Docker first.")
            return False
        
        client = docker.from_env()
        
        # Check if the container exists
        try:
            container = client.containers.get('google_maps_mysql')
            
            # Check if the container is running
            if container.status != 'running':
                logger.info("MySQL container exists but is not running. Starting it...")
                container.start()
                logger.info("MySQL container started")
                print("✓ MySQL container started")
                
                # Wait for MySQL to be ready
                logger.info("Waiting for MySQL to be ready...")
                time.sleep(10)  # Simple wait - in production, use healthcheck
            else:
                logger.info("MySQL container is already running")
                print("✓ MySQL container is already running")
                
            return True
            
        except docker.errors.NotFound:
            # Container doesn't exist, need to build and run from Dockerfile
            logger.info("MySQL container does not exist. Building from Dockerfile...")
            print("MySQL container does not exist. Building from Dockerfile...")
            
            from db_config import DOCKER_BUILD_PATH, DOCKER_MYSQL_CONTAINER, DOCKER_MYSQL_IMAGE
            
            # Check if Dockerfile exists
            dockerfile_path = os.path.join(DOCKER_BUILD_PATH, 'Dockerfile')
            if not os.path.exists(dockerfile_path):
                logger.error(f"Dockerfile not found at {dockerfile_path}")
                print(f"✗ Dockerfile not found at {dockerfile_path}")
                return False
            
            try:
                # Build the image from Dockerfile
                logger.info("Building MySQL image from Dockerfile...")
                print("Building MySQL image from Dockerfile...")
                
                image, build_logs = client.images.build(
                    path=DOCKER_BUILD_PATH,
                    tag='google_maps_mysql:latest',
                    rm=True
                )
                
                # Run the container
                logger.info("Starting MySQL container...")
                print("Starting MySQL container...")
                
                container = client.containers.run(
                    'google_maps_mysql:latest',
                    name=DOCKER_MYSQL_CONTAINER,
                    detach=True,
                    ports={'3306/tcp': 3306},
                    volumes={
                        'mysql_data': {'bind': '/var/lib/mysql', 'mode': 'rw'}
                    }
                )
                
                logger.info("MySQL container started")
                print("✓ MySQL container started")
                
                # Wait for MySQL to be ready
                logger.info("Waiting for MySQL to be ready...")
                print("Waiting for MySQL to be ready...")
                time.sleep(15)  # Simple wait - in production, use healthcheck
                
                return True
                
            except docker.errors.BuildError as e:
                logger.error(f"Failed to build MySQL image: {e}")
                print(f"✗ Failed to build MySQL image: {e}")
                return False
                
            except docker.errors.APIError as e:
                logger.error(f"Docker API error: {e}")
                print(f"✗ Docker API error: {e}")
                return False
                
    except Exception as e:
        logger.error(f"Error managing MySQL container: {e}")
        print(f"✗ Error managing MySQL container: {e}")
        return False

def create_db_connection():
    """Create a connection to the MySQL database"""
    # Make sure the MySQL container is running
    if not start_mysql_container():
        logger.error("Failed to ensure MySQL container is running")
        return None
    
    # Get database configuration
    db_config = get_db_config()
    
    # Try to connect to the database
    max_retries = 5
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['user'],
                password=db_config['password'],
                database=db_config['database']
            )
            
            if connection.is_connected():
                logger.info(f"Connected to MySQL database: {db_config['database']}")
                return connection
            
        except Error as e:
            retry_count += 1
            logger.warning(f"Failed to connect to MySQL database (attempt {retry_count}/{max_retries}): {e}")
            
            if retry_count < max_retries:
                time.sleep(2)  # Wait before retrying
            else:
                logger.error(f"Failed to connect to MySQL database after {max_retries} attempts: {e}")
                print(f"✗ Failed to connect to MySQL database after {max_retries} attempts: {e}")
                return None
    
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
                distance_text VARCHAR(100),
                distance_value INT,
                duration_text VARCHAR(100),
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
                source VARCHAR(100)
            )
            ''')
            
            # Commit changes to create tables
            connection.commit()
            
            # Verify tables were created
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            
            if 'travel_time_logs' in table_names and 'api_logs' in table_names:
                logger.info(f"Database tables created successfully: {table_names}")
                print(f"✓ Database tables created successfully: {table_names}")
            else:
                logger.error(f"Failed to create all required tables. Found: {table_names}")
                print(f"✗ Failed to create all required tables. Found: {table_names}")
                
        except Error as e:
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
            VALUES (%s, %s, %s, %s)
            """
            # Format datetime for MySQL
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(query, (timestamp, level, message, source))
            connection.commit()
            return True
        except Error as e:
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
        # Ensure origins and destinations are lists
        if isinstance(origins, str):
            origins = [origins]
        if isinstance(destinations, str):
            destinations = [destinations]
            
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
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
                                VALUES (%s, %s, %s, %s)
                                """
                                cursor.execute(log_query, (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "INFO", log_msg, "record_travel_time"))
                            except Error as e:
                                logger.error(f"Failed to log to api_logs table: {e}")
                        else:
                            log_msg = f"Failed to get travel time from {origin} to {destination}: {status}"
                            logger.error(log_msg)
                    except Error as e:
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
        # Create cursor with dictionary=True to return dictionaries
        cursor = connection.cursor(dictionary=True)
        
        # Check if table exists
        cursor.execute("SHOW TABLES LIKE 'travel_time_logs'")
        if not cursor.fetchone():
            logger.error("travel_time_logs table does not exist")
            print("✗ travel_time_logs table does not exist")
            return []
        
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
        rows = cursor.fetchall()
        
        # The rows are already dictionaries with MySQL Connector's dictionary=True
        results = rows
        
        logger.info(f"Retrieved {len(results)} historical travel time records")
        print(f"Retrieved {len(results)} historical travel time records")
        
        # If no results, try checking total count in table
        if len(results) == 0:
            cursor.execute("SELECT COUNT(*) as count FROM travel_time_logs")
            count_row = cursor.fetchone()
            count = count_row['count'] if count_row else 0
            print(f"Note: There are {count} total records in the travel_time_logs table")
            
            if count > 0 and (origin or destination):
                print(f"Check if your filters (origin='{origin}', destination='{destination}') match the data in the table")
                # Print a sample of what's in the table
                cursor.execute("SELECT origin, destination FROM travel_time_logs LIMIT 3")
                sample = cursor.fetchall()
                print(f"Sample data in table: {sample}")
        
        return results
        
    except Error as e:
        logger.error(f"Error retrieving historical data: {e}")
        print(f"✗ Error retrieving historical data: {e}")
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
        # Create cursor with dictionary=True to return dictionaries
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
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Check if Docker is running
    if not check_docker_running():
        print("✗ Docker is not running. Please start Docker and try again.")
        exit(1)
    
    # Setup database tables
    setup_database()
    
    # Log startup
    startup_msg = "Database logger started"
    logger.info(startup_msg)
    log_to_database("INFO", startup_msg)
    
    # Record initial travel times
    try:
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        if not api_key:
            print("⚠ Warning: GOOGLE_MAPS_API_KEY not found in environment variables")
            logger.warning("GOOGLE_MAPS_API_KEY not found in environment variables")
        else:
            origins = ["Seattle, WA"]
            destinations = ["San Francisco, CA", "Portland, OR"]
            record_travel_time(origins, destinations, api_key)
    except Error as e:
        logger.error(f"Error during initial travel time recording: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during initial travel time recording: {str(e)}")
    
    print("\nDatabase logger is ready. Starting scheduler...")
    
    # Start the scheduler
    try:
        start_scheduler()
    except KeyboardInterrupt:
        print("\nScheduler stopped by user.")
        logger.info("Scheduler stopped by user.")
    except Exception as e:
        print(f"\n✗ Error in scheduler: {str(e)}")
        logger.error(f"Error in scheduler: {str(e)}")
