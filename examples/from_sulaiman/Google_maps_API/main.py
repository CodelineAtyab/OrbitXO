"""
Main Application Entry Point

This script integrates all components of the Google Maps API tracking system:
- Distance Matrix API interface
- Route Tracking
- Logging (file and database)
- Slack notifications

Run this script to execute the complete system.
"""
import os
import sys
import argparse
import logging
from datetime import datetime
import time

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/application.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("main")

def setup_environment():
    """Setup the environment and required directories"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')
        logger.info("Created logs directory")

    # Check for API key
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        logger.warning("GOOGLE_MAPS_API_KEY environment variable not set! Some features may not work correctly.")
    else:
        logger.info("Google Maps API key found in environment variables")

def run_distance_matrix(origin, destination):
    """Run distance matrix calculation between locations"""
    try:
        from distance_matrix import get_distance_matrix
        
        logger.info(f"Calculating distance matrix from {origin} to {destination}")
        result = get_distance_matrix(origin, destination)
        
        if result.get("status") == "OK":
            # Extract the relevant information from the first route
            element = result["rows"][0]["elements"][0]
            if element["status"] == "OK":
                distance = element["distance"]["text"]
                duration = element["duration"]["text"]
                logger.info(f"Distance: {distance}, Duration: {duration}")
                return result
            else:
                logger.error(f"Route calculation failed: {element['status']}")
        else:
            logger.error(f"Distance matrix API failed: {result.get('status')}")
        
        return result
    except Exception as e:
        logger.error(f"Error in distance matrix calculation: {str(e)}")
        return None

def run_route_tracker(origin, destination, continuous=False, interval=300):
    """Run route tracker to monitor routes"""
    try:
        from route_tracker import RouteTracker
        
        logger.info(f"Starting route tracker for {origin} to {destination}")
        tracker = RouteTracker(
            origin=origin,
            destination=destination,
            check_interval_seconds=interval if continuous else 0
        )
        
        # Perform route check
        route_data = tracker.check_route()
        
        if route_data:
            logger.info(f"Route check successful - Distance: {route_data['distance_text']}, "
                        f"Duration: {route_data['duration_text']}")
            
            if route_data['is_min_distance']:
                logger.info(f"New minimum distance recorded: {route_data['distance_text']}")
                
            if route_data['is_min_duration']:
                logger.info(f"New minimum duration recorded: {route_data['duration_text']}")
            
            # Start continuous tracking if requested
            if continuous:
                logger.info(f"Starting continuous tracking every {interval} seconds")
                tracker.start_continuous_tracking()
                return tracker  # Return tracker object so it can be stopped later
            
            return route_data
        else:
            logger.error("Route check failed - No data returned")
            return None
    except Exception as e:
        logger.error(f"Error in route tracker: {str(e)}")
        return None

def log_to_database(route_data, origin, destination):
    """Log route data to database"""
    try:
        from db_logger import setup_database, log_to_database as db_log, record_travel_time
        
        # Setup database tables - this will also ensure MySQL container is running
        logger.info("Setting up database tables")
        setup_database()
        
        # Log application event
        logger.info("Logging route tracking event to database")
        db_log("INFO", f"Route tracked from {origin} to {destination}", source="main")
        
        # Record travel time data
        logger.info("Recording travel time data to database")
        api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        success = record_travel_time(origin, destination, api_key)
        
        if success:
            logger.info("Database logging completed successfully")
        else:
            logger.warning("Database logging returned False - check MySQL connection")
            
        return success
    except Exception as e:
        logger.error(f"Error logging to database: {str(e)}")
        return False

def send_slack_notification(route_data, origin, destination):
    """Send notification to Slack"""
    try:
        from slack_notifier import send_slack_notification
        
        logger.info("Sending route update to Slack")
        
        # Prepare notification message
        message = (f"Route Update: {origin} to {destination}\n"
                   f"Distance: {route_data['distance_text']} ({route_data['distance_meters']} meters)\n"
                   f"Duration: {route_data['duration_text']} ({route_data['duration_seconds']} seconds)")
        
        # Add minimum notifications if applicable
        if route_data.get('is_min_distance'):
            message += "\n🏆 This is the shortest distance recorded so far!"
            
        if route_data.get('is_min_duration'):
            message += "\n⚡ This is the fastest route recorded so far!"
        
        # Send to Slack
        success = send_slack_notification(message, "Route Tracker")
        
        if success:
            logger.info("Slack notification sent successfully")
        else:
            logger.warning("Failed to send Slack notification")
            
        return success
    except Exception as e:
        logger.error(f"Error sending Slack notification: {str(e)}")
        return False

def run_complete_system(origin, destination, continuous=False, interval=300, slack_notify=True):
    """Run the complete tracking system with all components"""
    logger.info(f"Starting complete system for route {origin} to {destination}")
    
    # Step 1: Run distance matrix calculation
    matrix_result = run_distance_matrix(origin, destination)
    if not matrix_result:
        logger.error("Distance matrix calculation failed, cannot continue")
        return False
    
    # Step 2: Run route tracker
    route_data = run_route_tracker(origin, destination, continuous, interval)
    if not route_data:
        logger.error("Route tracker failed, cannot continue")
        return False
    
    if isinstance(route_data, dict):  # If not continuous mode
        # Step 3: Log to database
        db_success = log_to_database(route_data, origin, destination)
        if not db_success:
            logger.warning("Database logging failed")
        
        # Step 4: Send Slack notification if enabled
        if slack_notify:
            slack_success = send_slack_notification(route_data, origin, destination)
            if not slack_success:
                logger.warning("Slack notification failed")
    
    # Step 5: Import and use logger_implementation (optional, for compatibility)
    try:
        import logger_implementation
        logger.info("Imported logger_implementation module")
    except Exception as e:
        logger.warning(f"Could not import logger_implementation: {str(e)}")
    
    logger.info("Complete system execution finished successfully")
    return True

def display_route_info(route_data):
    """Display route information in the console"""
    if not route_data or not isinstance(route_data, dict):
        print("\nNo valid route data to display")
        return
    
    print("\n" + "="*50)
    print(f"ROUTE: {route_data['origin']} → {route_data['destination']}")
    print("="*50)
    print(f"Distance: {route_data['distance_text']} ({route_data['distance_meters']} meters)")
    print(f"Duration: {route_data['duration_text']} ({route_data['duration_seconds']} seconds)")
    
    if route_data.get('is_min_distance'):
        print("✓ This is the shortest distance recorded so far!")
    
    if route_data.get('is_min_duration'):
        print("✓ This is the fastest route recorded so far!")
    
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Google Maps Route Tracking System')
    
    parser.add_argument('--origin', '-o', type=str, default="Seattle, WA",
                        help='Origin location (default: Seattle, WA)')
    
    parser.add_argument('--destination', '-d', type=str, default="Portland, OR",
                        help='Destination location (default: Portland, OR)')
    
    parser.add_argument('--continuous', '-c', action='store_true',
                        help='Enable continuous tracking mode')
    
    parser.add_argument('--interval', '-i', type=int, default=300,
                        help='Check interval in seconds for continuous mode (default: 300)')
    
    parser.add_argument('--no-slack', action='store_true',
                        help='Disable Slack notifications')
    
    return parser.parse_args()

def print_welcome():
    """Print welcome message and usage information"""
    print("""
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║               GOOGLE MAPS ROUTE TRACKING SYSTEM            ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝

This system:
1. Calculates distance and duration between locations
2. Tracks minimum distances and durations over time
3. Saves all data to a SQLite database
4. Can send notifications to Slack (if configured)

For more options, run: python main.py --help
For detailed documentation, see main_usage.md
""")

if __name__ == "__main__":
    # Setup environment
    setup_environment()
    logger.info("Starting Google Maps Route Tracking System")
    
    # Print welcome message
    print_welcome()
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Print startup information
    print("\nGoogle Maps Route Tracking System")
    print(f"Tracking route from {args.origin} to {args.destination}")
    if args.continuous:
        print(f"Mode: Continuous tracking (every {args.interval} seconds)")
    else:
        print("Mode: One-time check")
    
    # Run the complete system
    if args.continuous:
        print("Starting continuous tracking. Press Ctrl+C to stop.")
        try:
            tracker = run_route_tracker(args.origin, args.destination, True, args.interval)
            # Keep the main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nStopping tracking...")
            if tracker:
                tracker.stop_continuous_tracking()
            print("Tracking stopped.")
    else:
        result = run_complete_system(
            args.origin, 
            args.destination, 
            False, 
            args.interval, 
            not args.no_slack
        )
        
        if not result:
            print("System execution failed. Check logs for details.")
            sys.exit(1)
