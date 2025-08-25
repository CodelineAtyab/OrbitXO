import logging
import os
import json
import sys
import sqlite3
from logging.handlers import RotatingFileHandler
# Import database logger functionality
from db_logger import setup_database, log_to_database, record_travel_time, get_historical_data
# We'll import route_tracker inside the function to avoid circular imports

# Configure basic logging to a file
logging.basicConfig(filename='api2_logger.logs', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logging.basicConfig(
    filename='api2_logger.logs',
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
    handlers=[
        RotatingFileHandler(
            "./app.log",
            maxBytes=10 * 1024 * 1024,  # 10 MB
            backupCount=7,
            encoding="utf-8",
            mode="a"
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def run_route_tracker(origin="Seattle, WA", destination="Portland, OR", continuous=False, interval=0):
    """
    Run route tracker to track routes between specified locations.
    
    Args:
        origin (str): Origin location
        destination (str): Destination location
        continuous (bool): Whether to track continuously
        interval (int): Interval between checks in seconds (for continuous tracking)
    
    Returns:
        dict: Route data from the check
    """
    try:
        # Import here to avoid circular imports
        from route_tracker import RouteTracker
        
        logger.info(f"Starting route tracker for {origin} to {destination}")
        
        # Create tracker instance
        tracker = RouteTracker(
            origin=origin,
            destination=destination,
            check_interval_seconds=interval if continuous else 0
        )
        
        # For demonstration, we'll just do a one-time check
        # even if continuous tracking is requested
        logger.info("Performing one-time route check")
        log_to_database("INFO", f"Performing route check from {origin} to {destination}", source="run_route_tracker")
        route_data = tracker.check_route()
        
        if route_data:
            logger.info(f"Route check successful - Distance: {route_data['distance_text']}, Duration: {route_data['duration_text']}")
            log_to_database("INFO", f"Route check successful - Distance: {route_data['distance_text']}, Duration: {route_data['duration_text']}", source="run_route_tracker")
            
            # Log minimum values if applicable
            if route_data['is_min_distance']:
                logger.info(f"New minimum distance recorded: {route_data['distance_text']}")
                log_to_database("INFO", f"New minimum distance recorded: {route_data['distance_text']}", source="run_route_tracker")
            
            if route_data['is_min_duration']:
                logger.info(f"New minimum duration recorded: {route_data['duration_text']}")
                log_to_database("INFO", f"New minimum duration recorded: {route_data['duration_text']}", source="run_route_tracker")
                
            return route_data
        else:
            logger.error("Route check failed - No data returned")
            log_to_database("ERROR", "Route check failed - No data returned", source="run_route_tracker")
            return None
            
    except Exception as e:
        error_message = f"Exception occurred while running route tracker: {str(e)}"
        logger.error(error_message)
        log_to_database("ERROR", error_message, source="run_route_tracker")
        raise

if __name__ == "__main__":
    logger.debug("Debugging information: Starting the route tracker application")
    logger.warning("Warning: Ensure that the API key is set in the environment variables")
    logger.info("Starting route tracker application")
    
    print("Checking database connection...")
    
    # Setup database tables
    try:
        # Run the database check utility
        from database_check import check_database_connection
        check_database_connection()
        
        setup_database()
        print("Database tables setup complete")
        
        # Log application startup to database
        log_to_database("INFO", "Route tracker application started", source="logger_implementation")
        print("Successfully logged startup to database")
    except Exception as e:
        logger.error(f"Database setup error: {str(e)}")
        print(f"Database setup error: {str(e)}")
    
    # Example locations
    origin = "Seattle, WA"
    destination = "Portland, OR"
    
    # Run route tracker with example locations
    result = run_route_tracker(origin, destination)
    logger.info("Route tracker application completed")
    
    if result:
        # Display route information
        print("\n--- Route Information ---")
        print(f"From: {result['origin']}")
        print(f"To: {result['destination']}")
        print(f"Distance: {result['distance_text']} ({result['distance_meters']} meters)")
        print(f"Duration: {result['duration_text']} ({result['duration_seconds']} seconds)")
        
        if result['is_min_distance']:
            print("✓ This is the shortest distance recorded so far!")
        
        if result['is_min_duration']:
            print("✓ This is the fastest route recorded so far!")
            
        # Record travel time data to database
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        try:
            print("\n--- Recording Data to Database ---")
            record_travel_time([origin], [destination], api_key)
            print("✓ Route data successfully recorded to database")
            
            # Log results to database
            log_to_database(
                "INFO", 
                f"Route tracked from {origin} to {destination}: Distance {result['distance_text']}, Duration {result['duration_text']}", 
                source="logger_implementation"
            )
            
            # Give a small delay to ensure data is committed to database
            import time
            time.sleep(1)
            
            # Record travel time data to database
            print("\n--- Recording Data to Database ---")
            try:
                api_key = os.getenv("GOOGLE_MAPS_API_KEY")
                record_travel_time([origin], [destination], api_key)
                print("✓ Route data successfully recorded to database")
            except Exception as e:
                print(f"✗ Failed to record to database: {e}")
                
            # Example of retrieving historical data
            print("\n--- Recent Historical Data for this Route ---")
            try:
                historical_data = get_historical_data(origin=origin, destination=destination, limit=5)
                if historical_data:
                    for record in historical_data:
                        print(f"Time: {record['timestamp']} - Duration: {record['duration_text']}")
                else:
                    print("No historical data found in database.")
            except Exception as e:
                print(f"✗ Error retrieving historical data: {e}")
                
            print("Database connection check:")
            # Directly use db_logger's create_connection function to check connection
            try:
                from db_logger import create_db_connection
                connection = create_db_connection()
                if connection:
                    print("✓ Database connection successful")
                    # Configure SQLite connection to return dictionaries
                    connection.row_factory = sqlite3.Row
                    cursor = connection.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                    tables = cursor.fetchall()
                    print(f"Available tables: {[table[0] for table in tables]}")
                    cursor.close()
                    connection.close()
                else:
                    print("✗ Database connection failed")
            except Exception as e:
                print(f"✗ Database connection error: {e}")
        except Exception as e:
            print(f"Database operation error: {str(e)}")
            logger.error(f"Database operation error: {str(e)}")
    else:
        print("\nNo route data available.")
        log_to_database("ERROR", "Route tracking failed - No data returned", source="logger_implementation")