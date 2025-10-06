import mysql.connector
from datetime import datetime
from typing import Any, Dict, List, Optional

class SQLLogger:
    def __init__(
        self,
        host: str = "mysql-db",
        user: str = "root",
        password: str = "root",
        database: str = "api_log_db"
    ):
        self.connection_params = {
            "host": host,
            "user": user,
            "password": password,
            "database": database
        }

    def get_connection(self) -> mysql.connector.MySQLConnection:
        """Create and return a new database connection."""
        return mysql.connector.connect(**self.connection_params)

    def log_conversion(self, input_string: str, output_data: Any) -> None:
        """
        Log a measurement conversion to the database.
        
        Args:
            input_string: The original input string
            output_data: The conversion result
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            query = """
                INSERT INTO requests_log 
                (timestamp, input_string, output_data) 
                VALUES (%s, %s, %s)
            """
            values = (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                input_string,
                str(output_data)
            )
            
            cursor.execute(query, values)
            conn.commit()
        
        except mysql.connector.Error as err:
            print(f"Error logging conversion: {err}")
            raise
        
        finally:
            cursor.close()
            conn.close()

    def get_conversion_history(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve conversion history from the database.
        
        Args:
            limit: Optional maximum number of records to return
            offset: Optional number of records to skip
        
        Returns:
            List of conversion records
        """
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = "SELECT * FROM requests_log ORDER BY timestamp DESC"
            if limit is not None:
                query += f" LIMIT {limit}"
                if offset is not None:
                    query += f" OFFSET {offset}"
            
            cursor.execute(query)
            return cursor.fetchall()
        
        except mysql.connector.Error as err:
            print(f"Error retrieving conversion history: {err}")
            raise
        
        finally:
            cursor.close()
            conn.close()

    def clear_old_logs(self, days: int) -> int:
        """
        Remove logs older than specified number of days.
        
        Args:
            days: Number of days to keep logs for
        
        Returns:
            Number of records deleted
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            query = """
                DELETE FROM requests_log 
                WHERE timestamp < DATE_SUB(NOW(), INTERVAL %s DAY)
            """
            cursor.execute(query, (days,))
            deleted_count = cursor.rowcount
            conn.commit()
            return deleted_count
        
        except mysql.connector.Error as err:
            print(f"Error clearing old logs: {err}")
            raise
        
        finally:
            cursor.close()
            conn.close()

# Create a default logger instance
sql_logger = SQLLogger()