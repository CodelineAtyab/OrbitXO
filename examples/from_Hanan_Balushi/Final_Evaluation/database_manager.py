import mysql.connector
import os
import json
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger('measurement_api.database')

class DatabaseManager:
    """Manages database operations for conversion history"""
    
    def __init__(self):
        self.config = {
            'host': os.getenv('DB_HOST', 'mysql'),
            'port': int(os.getenv('DB_PORT', '3306')),
            'user': os.getenv('DB_USER', 'measurement_user'),
            'password': os.getenv('DB_PASSWORD', 'measurement_pass'),
            'database': os.getenv('DB_NAME', 'measurement_db')
        }
        self.connection = None
    
    def _get_connection(self):
        """Get or create database connection"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(**self.config)
                logger.info("Database connection established")
            return self.connection
        except mysql.connector.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def initialize_database(self):
        """Create the history table if it doesn't exist"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            create_table_query = """
            CREATE TABLE IF NOT EXISTS conversion_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                input_string TEXT NOT NULL,
                result JSON NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_timestamp (timestamp)
            )
            """
            
            cursor.execute(create_table_query)
            conn.commit()
            cursor.close()
            
            logger.info("Database table initialized successfully")
        except mysql.connector.Error as e:
            logger.error(f"Failed to initialize database: {e}")
            raise
    
    def save_conversion(self, input_string: str, result: List[int]):
        """
        Save a conversion to the history table
        
        Args:
            input_string: The input measurement string
            result: The conversion result (list of integers)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            insert_query = """
            INSERT INTO conversion_history (input_string, result, timestamp)
            VALUES (%s, %s, %s)
            """
            
            result_json = json.dumps(result)
            timestamp = datetime.now()
            
            cursor.execute(insert_query, (input_string, result_json, timestamp))
            conn.commit()
            cursor.close()
            
            logger.info(f"Saved conversion to database: {input_string} -> {result}")
        except mysql.connector.Error as e:
            logger.error(f"Failed to save conversion: {e}")
            raise
    
    def get_history(self, limit: int = 100) -> List[Dict]:
        """
        Retrieve conversion history from the database
        
        Args:
            limit: Maximum number of records to retrieve
            
        Returns:
            List of dictionaries containing history records
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(dictionary=True)
            
            query = """
            SELECT id, input_string, result, timestamp
            FROM conversion_history
            ORDER BY timestamp DESC
            LIMIT %s
            """
            
            cursor.execute(query, (limit,))
            rows = cursor.fetchall()
            cursor.close()
            
            # Parse JSON result field
            history = []
            for row in rows:
                history.append({
                    'id': row['id'],
                    'input_string': row['input_string'],
                    'result': json.loads(row['result']),
                    'timestamp': row['timestamp'].isoformat()
                })
            
            logger.info(f"Retrieved {len(history)} history records")
            return history
        except mysql.connector.Error as e:
            logger.error(f"Failed to retrieve history: {e}")
            raise
    
    def close(self):
        """Close the database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")