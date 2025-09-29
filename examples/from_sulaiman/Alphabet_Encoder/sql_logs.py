from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime
import json
import time
import pymysql
import logging
from logging.handlers import RotatingFileHandler
import sys

# Get MySQL connection details from environment variables
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'password')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'alphabet_logs')

# Create MySQL connection URI
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"

# Set up log directory
LOG_DIR = os.environ.get('LOG_DIR', 'logs')
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configure logging
# Logger for application logs
app_logger = logging.getLogger(__name__)
app_logger.setLevel(logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)

# File handler for application logs
app_file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, 'app.log'),
    maxBytes=10485760,  # 10MB
    backupCount=10
)
app_file_handler.setLevel(logging.INFO)
app_file_handler.setFormatter(console_format)

# Add handlers to logger
app_logger.addHandler(console_handler)
app_logger.addHandler(app_file_handler)

# Dedicated logger for API request/response logs
api_logger = logging.getLogger("api_requests")
api_logger.setLevel(logging.INFO)

# File handler for API logs
api_file_handler = RotatingFileHandler(
    os.path.join(LOG_DIR, 'api_requests.log'),
    maxBytes=10485760,  # 10MB
    backupCount=10
)
api_file_handler.setLevel(logging.INFO)
api_format = logging.Formatter('%(asctime)s - %(message)s')
api_file_handler.setFormatter(api_format)
api_logger.addHandler(api_file_handler)

# Use app_logger instead of logger
logger = app_logger

# Function to wait for database to be available
def wait_for_db(max_retries=60, retry_interval=1):
    """Wait for the database to be available."""
    logger.info(f"Waiting for database at {MYSQL_HOST}...")
    
    retries = 0
    while retries < max_retries:
        try:
            connection = pymysql.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=MYSQL_PASSWORD
            )
            connection.close()
            logger.info("Database is available!")
            return True
        except pymysql.Error:
            retries += 1
            if retries < max_retries:
                logger.info(f"Database not available yet. Retry {retries}/{max_retries}...")
                time.sleep(retry_interval)
    
    logger.error(f"Failed to connect to database after {max_retries} attempts")
    return False

# Create SQLAlchemy engine with retry support
def get_engine():
    if wait_for_db():
        try:
            return create_engine(DATABASE_URL)
        except Exception as e:
            logger.error(f"Error creating database engine: {e}")
            raise
    else:
        raise Exception("Could not connect to the database")

# Create the engine
engine = get_engine()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define the Log model
class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    input = Column(Text)
    output = Column(Text)
    
# Create the tables
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise

# Function to log API requests
def log_request(input_str, output_result):
    # Log to database
    db = SessionLocal()
    try:
        # Create log entry for database
        log = Log(
            input=input_str,
            output=json.dumps(output_result)
        )
        db.add(log)
        db.commit()
        db.refresh(log)
        
        # Log to file
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = {
            "timestamp": timestamp,
            "input": input_str,
            "output": output_result
        }
        api_logger.info(json.dumps(log_message))
        
        logger.info(f"Request logged: input='{input_str}', output={output_result}")
        return log
    except Exception as e:
        db.rollback()
        logger.error(f"Error logging request: {e}")
        return None
    finally:
        db.close()
