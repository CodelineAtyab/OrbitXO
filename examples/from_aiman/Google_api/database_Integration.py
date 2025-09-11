import os
import sys
import time
import datetime
import json
import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor
import logging

from logging_implementation import LoggingConfig, LogExecutionTime, log_function_call
from google_maps_api import get_travel_time

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'travel_times.db')

class TravelTimeDatabase:
    
    def __init__(self, db_path=DB_PATH, logging_config=None):
        self.db_path = db_path
        
        if logging_config is None:
            self.logging_config = LoggingConfig(
                app_name="travel_db",
                log_level=logging.INFO
            )
        else:
            self.logging_config = logging_config
            
        self.logger = self.logging_config.get_component_logger("database")
        
        self._init_db()
    
    def _init_db(self):
        with LogExecutionTime(self.logger, "database initialization"):
            try:
                conn = sqlite3.connect(self.db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS locations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                ''')
                
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS routes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id INTEGER NOT NULL,
                    destination_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_id) REFERENCES locations (id),
                    FOREIGN KEY (destination_id) REFERENCES locations (id),
                    UNIQUE (source_id, destination_id)
                )
                ''')
                
                cursor.execute('''
                CREATE TABLE IF NOT EXISTS travel_times (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    route_id INTEGER NOT NULL,
                    duration_seconds INTEGER NOT NULL,
                    distance_meters INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (route_id) REFERENCES routes (id)
                )
                ''')
                
                conn.commit()
                self.logger.info("Database tables created successfully")
                
            except sqlite3.Error as e:
                self.logger.error(f"Database initialization error: {str(e)}")
                raise
            finally:
                if conn:
                    conn.close()
    
    def _get_location_id(self, location_name, conn):
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM locations WHERE name = ?", (location_name,))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        
        cursor.execute("INSERT INTO locations (name) VALUES (?)", (location_name,))
        conn.commit()
        
        return cursor.lastrowid
    
    def _get_route_id(self, source_id, destination_id, conn):
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM routes WHERE source_id = ? AND destination_id = ?", 
                      (source_id, destination_id))
        result = cursor.fetchone()
        
        if result:
            return result[0]
        
        cursor.execute("INSERT INTO routes (source_id, destination_id) VALUES (?, ?)", 
                      (source_id, destination_id))
        conn.commit()
        
        return cursor.lastrowid
        conn.commit()
        
        return cursor.lastrowid
    
    @log_function_call(logging.getLogger("database"))
    def record_travel_time(self, source, destination, duration_seconds, distance_meters):
        self.logger.info(f"Recording travel time: {source} -> {destination}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            
            source_id = self._get_location_id(source, conn)
            destination_id = self._get_location_id(destination, conn)
            
            route_id = self._get_route_id(source_id, destination_id, conn)
            
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO travel_times (route_id, duration_seconds, distance_meters)
            VALUES (?, ?, ?)
            ''', (route_id, duration_seconds, distance_meters))
            
            conn.commit()
            
            self.logger.info(f"Recorded travel time: {duration_seconds//60} minutes ({source} -> {destination})")
            return True
            
        except sqlite3.Error as e:
            self.logger.error(f"Error recording travel time: {str(e)}")
            return False
        finally:
            if conn:
                conn.close()
    
    @log_function_call(logging.getLogger("database"))
    def get_historical_data(self, source, destination, date=None):
        self.logger.info(f"Retrieving historical data for {source} -> {destination}")
        
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = '''
            SELECT tt.timestamp, tt.duration_seconds, tt.distance_meters
            FROM travel_times tt
            JOIN routes r ON tt.route_id = r.id
            JOIN locations src ON r.source_id = src.id
            JOIN locations dst ON r.destination_id = dst.id
            WHERE src.name = ? AND dst.name = ?
            '''
            
            params = [source, destination]
            
            if date:
                query += " AND date(tt.timestamp) = date(?)"
                params.append(date)
            
            query += " ORDER BY tt.timestamp"
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            results = []
            for row in rows:
                results.append({
                    'timestamp': row['timestamp'],
                    'duration_minutes': row['duration_seconds'] // 60,
                    'distance_km': row['distance_meters'] / 1000,
                })
            
            self.logger.info(f"Retrieved {len(results)} historical records")
            return results
            
        except sqlite3.Error as e:
            self.logger.error(f"Error retrieving historical data: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()
    
    def format_historical_data(self, data, format_type='text'):
        if not data:
            return "No data available."
        
        if format_type == 'json':
            return json.dumps(data, indent=2)
        
        first_timestamp = data[0]['timestamp']
        date_str = first_timestamp.split(' ')[0]
        
        output = [f"Date: {date_str}"]
        
        for record in data:
            timestamp = record['timestamp'].split(' ')[1][:8]
            duration = record['duration_minutes']
            output.append(f"{timestamp} - {duration} minutes")
        
        return "\n".join(output)


class TravelTimeTracker:
    
    def __init__(self, sources_destinations=None, api_key=None, interval_minutes=15):
        # Set up logging
        self.logging_config = LoggingConfig(
            app_name="travel_tracker",
            log_level=logging.INFO
        )
        self.logger = self.logging_config.get_default_logger()
        
        # Initialize the database
        self.db = TravelTimeDatabase(logging_config=self.logging_config)
        
        # Default sources and destinations if none provided
        if not sources_destinations:
            # Try to load from config.json
            try:
                current_dir = os.path.dirname(os.path.abspath(__file__))
                config_path = os.path.join(current_dir, "config.json")
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    source = config.get("source", "Muscat, Oman")
                    destination = config.get("destination", "Salalah, Oman")
                    sources_destinations = [(source, destination)]
            except:
                # Use default values
                sources_destinations = [("Muscat, Oman", "Salalah, Oman")]
        
        self.sources_destinations = sources_destinations
        self.api_key = api_key
        self.interval_minutes = interval_minutes
        
        # Initialize scheduler
        executors = {
            'default': ThreadPoolExecutor(max_workers=5)
        }
        self.scheduler = BackgroundScheduler(executors=executors)
    
    @log_function_call(logging.getLogger("tracker"))
    def track_travel_time(self):
        self.logger.info("Running scheduled travel time tracking")
        
        for source, destination in self.sources_destinations:
            try:
                with LogExecutionTime(self.logger, f"travel time tracking for {source} -> {destination}"):
                    # Get travel time from Google Maps API
                    try:
                        result = get_travel_time(source, destination, self.api_key)
                        
                        if result.get("success", False):
                            # Extract duration and distance
                            duration_seconds = result.get("duration_value")
                            distance_meters = result.get("distance_value")
                            
                            # Record in database
                            self.db.record_travel_time(
                                source,
                                destination,
                                duration_seconds,
                                distance_meters
                            )
                        else:
                            self.logger.error(f"Failed to get travel time: {result.get('error')}")
                    except ValueError as e:
                        self.logger.error(f"API Error: {str(e)}")
                        self.logger.info("Please make sure your API key is set in config.json or as an environment variable GOOGLE_MAPS_API_KEY")
                        return
            
            except Exception as e:
                self.logger.error(f"Error tracking travel time: {str(e)}")
    
    def start_tracking(self):
        self.logger.info(f"Starting travel time tracking every {self.interval_minutes} minutes")
        
        trigger = IntervalTrigger(minutes=self.interval_minutes)
        self.scheduler.add_job(
            self.track_travel_time,
            trigger=trigger,
            id='travel_time_tracking',
            replace_existing=True
        )
        
        self.scheduler.start()
        
        self.track_travel_time()
    
    def stop_tracking(self):
        self.logger.info("Stopping travel time tracking")
        self.scheduler.shutdown()
    
    @log_function_call(logging.getLogger("tracker"))
    def get_historical_data(self, source, destination, date=None, format_type='text'):
        data = self.db.get_historical_data(source, destination, date)
        
        return self.db.format_historical_data(data, format_type)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Track travel times between locations')
    parser.add_argument('--source', help='Source location')
    parser.add_argument('--destination', help='Destination location')
    parser.add_argument('--interval', type=int, default=15, help='Tracking interval in minutes')
    parser.add_argument('--historical', action='store_true', help='Retrieve historical data')
    parser.add_argument('--date', help='Date for historical data (YYYY-MM-DD)')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')
    parser.add_argument('--api-key', help='Google Maps API key')
    
    args = parser.parse_args()
    
    # Set up the tracker
    sources_destinations = None
    if args.source and args.destination:
        sources_destinations = [(args.source, args.destination)]
    
    tracker = TravelTimeTracker(
        sources_destinations=sources_destinations,
        interval_minutes=args.interval,
        api_key=args.api_key
    )
    
    # If historical data is requested
    if args.historical:
        if not args.source or not args.destination:
            print("Error: Source and destination are required for historical data")
            return
        
        data = tracker.get_historical_data(
            args.source,
            args.destination,
            args.date,
            args.format
        )
        print(data)
        return
    
    # Otherwise, start tracking
    try:
        tracker.start_tracking()
        print(f"Travel time tracking started. Press Ctrl+C to stop.")
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("Stopping travel time tracker...")
        tracker.stop_tracking()
        print("Tracker stopped.")


if __name__ == "__main__":
    main()
