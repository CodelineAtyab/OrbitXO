import os
import json
import logging
import sqlite3
from datetime import datetime
import time
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

def load_travel_times_from_json(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading travel times from JSON: {e}")
        return {}

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_database_connection():
    db_file = os.environ.get("DB_FILE", os.path.join(os.path.dirname(__file__), "travel_times.db"))
    try:
        connection = sqlite3.connect(db_file)
        connection.row_factory = dict_factory
        logger.info(f"Connected to SQLite database: {db_file}")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to SQLite database: {e}")
        raise

def create_tables(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS travel_times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                destination TEXT NOT NULL,
                duration REAL NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        logger.info("Database tables created successfully")
    except Exception as e:
        connection.rollback()
        logger.error(f"Error creating tables: {e}")
        raise

def format_duration(minutes):
    hours = int(minutes // 60)
    remaining_minutes = int(minutes % 60)
    if hours > 0:
        if remaining_minutes > 0:
            return f"{hours} hour{'s' if hours > 1 else ''} {remaining_minutes} minute{'s' if remaining_minutes > 1 else ''}"
        else:
            return f"{hours} hour{'s' if hours > 1 else ''}"
    else:
        return f"{remaining_minutes} minute{'s' if remaining_minutes > 1 else ''}"

def record_travel_time(connection, source, destination, duration):
    try:
        cursor = connection.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = """
            INSERT INTO travel_times (source, destination, duration, recorded_at)
            VALUES (?, ?, ?, ?)
        """
        cursor.execute(sql, (source, destination, duration, now))
        connection.commit()
        formatted_duration = format_duration(duration)
        logger.info(f"Recorded travel time: {formatted_duration} ({source} -> {destination}) at {now}")
        return True
        
    except Exception as e:
        connection.rollback()
        logger.error(f"Error recording travel time: {e}")
        return False

def get_historical_data(connection, source, destination, date_str):
    try:
        cursor = connection.cursor()
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        start_date = date_obj.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%d %H:%M:%S")
        end_date = date_obj.replace(hour=23, minute=59, second=59).strftime("%Y-%m-%d %H:%M:%S")
        
        sql = """
            SELECT * FROM travel_times 
            WHERE source = ? 
            AND destination = ? 
            AND recorded_at >= ? 
            AND recorded_at <= ?
            ORDER BY recorded_at
        """
        cursor.execute(sql, (source, destination, start_date, end_date))
        results = cursor.fetchall()
        historical_data = {
            "date": date_str,
            "route": f"{source} -> {destination}",
            "times": []
        }
        
        for record in results:
            dt = datetime.strptime(record["recorded_at"], "%Y-%m-%d %H:%M:%S")
            time_str = dt.strftime("%H:%M:%S")
            formatted_duration = format_duration(record["duration"])
        
            historical_data["times"].append({
                "time": time_str,
                "duration": record["duration"],
                "formatted_duration": formatted_duration
            })
        
        print(f"Date: {date_str}")
        for entry in historical_data["times"]:
            print(f"{entry['time']} - {entry['formatted_duration']}")
            
        return historical_data
    except Exception as e:
        logger.error(f"Error retrieving historical data: {e}")
        return None

def record_current_travel_times(connection, json_file_path):
    travel_times_data = load_travel_times_from_json(json_file_path)
    
    logger.info("Connected to SQLite database")
    
    for _, route_data in travel_times_data.items():
        source = route_data.get("source", "")
        destination = route_data.get("destination", "")
        duration = route_data.get("min_duration", 0)
        
        record_travel_time(connection, source, destination, duration)
    
    logger.info("Recording complete")

def setup_scheduler(json_file_path):
    scheduler = BackgroundScheduler()
    
    def scheduled_job():
        try:
            connection = get_database_connection()
            record_current_travel_times(connection, json_file_path)
            connection.close()
        except Exception as e:
            logger.error(f"Error in scheduled job: {e}")
    
    scheduler.add_job(
        scheduled_job, 
        'interval', 
        minutes=15
    )
    
    scheduler.start()
    logger.info("Scheduler started - recording travel times every 15 minutes")
    
    return scheduler

def store_in_json_file(data, file_path):
    try:
        existing_data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                existing_data = json.load(f)
        
        existing_data.update(data)
        
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=2)
        
        logger.info(f"Data stored in JSON file: {file_path}")
    except Exception as e:
        logger.error(f"Error storing data in JSON file: {e}")

def is_sqlite_available():
    try:
        import sqlite3
        conn = sqlite3.connect(':memory:')
        conn.close()
        return True
    except Exception:
        return False

if __name__ == "__main__":
    json_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'travel_times.json')
    
    sqlite_available = is_sqlite_available()
    
    if sqlite_available:
        try:
            connection = get_database_connection()
            
            create_tables(connection)
            
            scheduler = setup_scheduler(json_file_path)
            
            try:
                record_current_travel_times(connection, json_file_path)
                
                connection.close()
                
                logger.info("Travel time monitoring is running with SQLite. Press Ctrl+C to stop.")
                while True:
                    time.sleep(60)
                    
            except KeyboardInterrupt:
                scheduler.shutdown()
                logger.info("Scheduler stopped")
                
        except Exception as e:
            logger.error(f"Error with SQLite database: {e}")
            sqlite_available = False
    
    if not sqlite_available:
        logger.warning("SQLite is not available. Falling back to JSON file storage.")
        
        travel_times = load_travel_times_from_json(json_file_path)
        
        def json_update_job():
            new_data = load_travel_times_from_json(json_file_path)
            for key, route_data in new_data.items():
                if 'history' not in route_data:
                    route_data['history'] = []
                
                duration = route_data.get("min_duration", 0)
                formatted_duration = format_duration(duration)
                
                route_data['history'].append({
                    "duration": duration,
                    "formatted_duration": formatted_duration,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            
            store_in_json_file(new_data, json_file_path)
            logger.info("Updated travel times in JSON file")
        
        fallback_scheduler = BackgroundScheduler()
        fallback_scheduler.add_job(json_update_job, 'interval', minutes=15)
        fallback_scheduler.start()
        
        try:
            json_update_job()
            
            logger.info("Travel time monitoring is running in JSON-only mode. Press Ctrl+C to stop.")
            while True:
                time.sleep(60)
                
        except KeyboardInterrupt:
            fallback_scheduler.shutdown()
            logger.info("Scheduler stopped")
