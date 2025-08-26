import os
import sqlalchemy
from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, Boolean, Float, text, create_engine
import datetime
import logging

_logger = logging.getLogger("db_connector")
_engine = None
_conn = None
_metadata = MetaData()

travel_time_history = Table(
    'travel_time_history', _metadata,
    Column('id', Integer, primary_key=True),
    Column('timestamp', DateTime, nullable=False),
    Column('source', String(255), nullable=False),
    Column('destination', String(255), nullable=False),
    Column('duration_minutes', Integer, nullable=False),
    Column('distance', String(100)),
    Column('distance_value', Integer),
    Column('is_minimum', Boolean, default=False)
)

def initialize_connection():
    global _engine, _conn, _metadata
    try:
        # Create database directory if it doesn't exist
        db_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database")
        os.makedirs(db_dir, exist_ok=True)
        
        # Use SQLite instead of MySQL
        db_path = os.path.join(db_dir, "travel_time.db")
        _logger.info(f"Using SQLite database at {db_path}")
        
        connection_string = f"sqlite:///{db_path}"
        _engine = create_engine(connection_string, echo=False)
        
        # Create tables
        _metadata.create_all(_engine)
        _conn = _engine.connect()
        _logger.info("Database connection initialized")
        return True
    except Exception as e:
        _logger.error(f"Database connection failed: {e}")
        return False

def add_travel_time_record(source, destination, duration_minutes, distance=None, distance_value=None, is_minimum=False):
    global _engine, _conn
    
    if _engine is None:
        if not initialize_connection():
            return False
        
    try:
        ins = travel_time_history.insert().values(
            timestamp=datetime.datetime.now(),
            source=source,
            destination=destination,
            duration_minutes=duration_minutes,
            distance=distance,
            distance_value=distance_value,
            is_minimum=is_minimum
        )
        
        with _engine.begin() as conn:
            conn.execute(ins)
            
        _logger.info(f"Added travel time record: {source} to {destination}, {duration_minutes} minutes")
        return True
        
    except Exception as e:
        _logger.error(f"Failed to add travel time record: {e}")
        return False

def get_travel_time_history(source=None, destination=None, start_date=None, end_date=None, limit=100):
    global _engine
    
    if _engine is None:
        if not initialize_connection():
            return []
        
    try:
        query = sqlalchemy.select([travel_time_history])
        
        if source:
            query = query.where(travel_time_history.c.source == source)
        if destination:
            query = query.where(travel_time_history.c.destination == destination)
        if start_date:
            query = query.where(travel_time_history.c.timestamp >= start_date)
        if end_date:
            query = query.where(travel_time_history.c.timestamp <= end_date)
            
        query = query.order_by(travel_time_history.c.timestamp.desc()).limit(limit)
        
        with _engine.connect() as conn:
            result = conn.execute(query)
            records = [dict(row) for row in result]
            
        _logger.info(f"Retrieved {len(records)} travel time records")
        return records
        
    except Exception as e:
        _logger.error(f"Failed to retrieve travel time history: {e}")
        return []

def get_minimum_travel_times(source=None, destination=None):
    global _engine
    
    if _engine is None:
        if not initialize_connection():
            return []
        
    try:
        sql = """
        SELECT source, destination, MIN(duration_minutes) as min_duration
        FROM travel_time_history
        """
        
        params = {}
        where_clauses = []
        
        if source:
            where_clauses.append("source = :source")
            params["source"] = source
        if destination:
            where_clauses.append("destination = :destination")
            params["destination"] = destination
            
        if where_clauses:
            sql += " WHERE " + " AND ".join(where_clauses)
            
        sql += " GROUP BY source, destination"
        
        with _engine.connect() as conn:
            result = conn.execute(text(sql), params)
            records = [dict(row) for row in result]
        
        _logger.info(f"Retrieved {len(records)} minimum travel time records")
        return records
        
    except Exception as e:
        _logger.error(f"Failed to retrieve minimum travel times: {e}")
        return []

def get_db_connector():
    if _engine is None:
        if not initialize_connection():
            _logger.error("Failed to initialize database connection")
            # Return functions that will handle errors gracefully
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