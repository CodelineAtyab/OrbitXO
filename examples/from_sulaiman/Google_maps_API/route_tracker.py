import json
import time
from datetime import datetime
import csv
import os
import logging
from distance_matrix import get_distance_matrix
from slack_notifier import send_slack_notification
from logger_implementation import logger

class RouteTracker:
    """
    A class for tracking the minimum distance and time between two locations over time.
    """
    
    def __init__(self, origin, destination, output_file="route_tracking.csv", check_interval_seconds=0):
        """
        Initialize the route tracker.
        
        Args:
            origin (str): The starting location
            destination (str): The destination location
            output_file (str): File to save the tracking data
            check_interval_seconds (int): Time between checks in seconds (0 for one-time check)
        """
        self.origin = origin
        self.destination = destination
        self.output_file = output_file
        self.check_interval_seconds = check_interval_seconds
        
        # Track minimum values
        self.min_distance = float('inf')
        self.min_duration = float('inf')
        self.min_distance_timestamp = None
        self.min_duration_timestamp = None
        
        # Initialize CSV file if it doesn't exist
        if not os.path.exists(output_file):
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'Origin', 'Destination', 'Distance (meters)', 
                                'Distance (text)', 'Duration (seconds)', 'Duration (text)', 
                                'Is Min Distance', 'Is Min Duration'])
    
    def check_route(self):
        """
        Check the current route conditions and record the data.
        
        Returns:
            dict: The route data or None if there was an error
        """
        print(f"Checking route from {self.origin} to {self.destination}...")
        
        try:
            # Get the route information
            result = get_distance_matrix(self.origin, self.destination)
            
            if result.get("status") == "OK" and result["rows"][0]["elements"][0]["status"] == "OK":
                # Extract the route data
                element = result["rows"][0]["elements"][0]
                distance_meters = element["distance"]["value"]
                distance_text = element["distance"]["text"]
                duration_seconds = element["duration"]["value"]
                duration_text = element["duration"]["text"]
                
                # Check if this is a new minimum
                is_min_distance = False
                is_min_duration = False
                
                if distance_meters < self.min_distance:
                    self.min_distance = distance_meters
                    self.min_distance_timestamp = datetime.now()
                    is_min_distance = True
                    
                if duration_seconds < self.min_duration:
                    self.min_duration = duration_seconds
                    self.min_duration_timestamp = datetime.now()
                    is_min_duration = True
                
                # Also store these as separate attributes with consistent naming
                # This ensures API compatibility
                self.distance_meters = distance_meters
                self.duration_seconds = duration_seconds
                
                # Current timestamp
                now = datetime.now()
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                
                # Record data
                with open(self.output_file, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([
                        timestamp,
                        self.origin,
                        self.destination,
                        distance_meters,
                        distance_text,
                        duration_seconds,
                        duration_text,
                        is_min_distance,
                        is_min_duration
                    ])
                
                # Create route data dictionary
                route_data = {
                    "timestamp": timestamp,
                    "origin": self.origin,
                    "destination": self.destination,
                    "distance_meters": distance_meters,
                    "distance_text": distance_text,
                    "duration_seconds": duration_seconds,
                    "duration_text": duration_text,
                    "is_min_distance": is_min_distance,
                    "is_min_duration": is_min_duration
                }
                
                # Log the route tracking
                tracking_type = "continuous" if self.check_interval_seconds > 0 else "one-time"
                logger.info(f"Route checked from {self.origin} to {self.destination} ({tracking_type}): "
                           f"Distance: {distance_text}, Duration: {duration_text}")
                
                if is_min_distance:
                    logger.info(f"New minimum distance found: {distance_text}")
                
                if is_min_duration:
                    logger.info(f"New minimum duration found: {duration_text}")
                
                return route_data
            else:
                error_message = "No route found"
                if "error_message" in result:
                    error_message = result["error_message"]
                print(f"Error: {error_message}")
                logger.error(f"Route check error: {error_message}")
                return None
                
        except Exception as e:
            error_msg = f"Error checking route: {str(e)}"
            print(error_msg)
            logger.error(f"Exception in route_tracker.check_route: {error_msg}")
            return None
    
    def track_continuously(self):
        """
        Track the route continuously at the specified interval.
        """
        if self.check_interval_seconds <= 0:
            # One-time check
            route_data = self.check_route()
            self.display_results(route_data)
            return
        
        print(f"Tracking route from {self.origin} to {self.destination} every {self.check_interval_seconds} seconds.")
        print("Press Ctrl+C to stop tracking.")
        
        try:
            while True:
                route_data = self.check_route()
                self.display_results(route_data)
                time.sleep(self.check_interval_seconds)
        except KeyboardInterrupt:
            print("\nTracking stopped by user.")
    
    def display_results(self, route_data):
        """
        Display the route results.
        """
        if not route_data:
            print("No route data available.")
            return
            
        print("\n--- Route Information ---")
        print(f"Time: {route_data['timestamp']}")
        print(f"From: {route_data['origin']}")
        print(f"To: {route_data['destination']}")
        print(f"Distance: {route_data['distance_text']} ({route_data['distance_meters']} meters)")
        print(f"Duration: {route_data['duration_text']} ({route_data['duration_seconds']} seconds)")
        
        if route_data['is_min_distance']:
            print("✓ This is the shortest distance recorded so far!")
        
        if route_data['is_min_duration']:
            print("✓ This is the fastest route recorded so far!")
            
        print(f"Results saved to {self.output_file}")
        
        # Send notification to Slack
        try:
            logger.info(f"Sending Slack notification for route: {route_data['origin']} to {route_data['destination']}")
            sent = send_slack_notification(route_data)
            if sent:
                print("✓ Slack notification sent successfully!")
                logger.info("Slack notification sent successfully")
            else:
                error_msg = "Failed to send Slack notification"
                print(f"✗ {error_msg}")
                logger.warning(f"Slack notification failed: {error_msg}")
        except Exception as e:
            error_msg = f"Error sending Slack notification: {str(e)}"
            print(f"✗ {error_msg}")
            logger.error(f"Exception in route_tracker.display_results: {error_msg}")


def main():
    print("Route Tracker - Track minimum distance and time between locations")
    print("===============================================================")
    
    # Get user input
    origin = input("Enter origin location: ").strip() or "Seattle, WA"
    destination = input("Enter destination location: ").strip() or "Portland, OR"
    
    # Ask if user wants continuous tracking
    track_continuously = input("Track continuously? (y/n): ").strip().lower() == 'y'
    
    interval = 0
    if track_continuously:
        try:
            interval = int(input("Enter check interval in seconds (minimum 60): ").strip())
            interval = max(60, interval)  # Ensure minimum interval of 60 seconds to avoid API rate limits
        except ValueError:
            interval = 300  # Default to 5 minutes
    
    # Create tracker
    tracker = RouteTracker(origin, destination, check_interval_seconds=interval)
    
    # Start tracking
    tracker.track_continuously()
    
    # Display summary if not continuous
    if not track_continuously:
        print("\n--- Tracking Summary ---")
        if tracker.min_distance_timestamp:
            print(f"Minimum distance: {tracker.min_distance} meters recorded at {tracker.min_distance_timestamp}")
        if tracker.min_duration_timestamp:
            print(f"Minimum duration: {tracker.min_duration} seconds recorded at {tracker.min_duration_timestamp}")

if __name__ == "__main__":
    main()
