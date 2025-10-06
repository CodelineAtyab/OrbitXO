import time
import mysql.connector
from fastapi import FastAPI
from parser import parse_measurement
from log_config import logger

# Wait for MySQL to be ready
db_ready = False
while not db_ready:
    try:
        conn = mysql.connector.connect(
            host="mysql-db",
            user="root",
            password="root",
            database="api_log_db"
        )
        conn.close()
        db_ready = True
        print("✅ MySQL is ready!")
    except mysql.connector.Error:
        print("⏳ Waiting for MySQL...")
        time.sleep(2)

# FastAPI setup
app = FastAPI()

# Initialize MySQL connection function
def get_db_connection():
    return mysql.connector.connect(
        host="mysql-db",
        user="root",
        password="root",
        database="api_log_db"
    )

@app.get("/convert-measurements")
def convert_measurements(input: str):
    logger.info(f"Received conversion request for: '{input}'")
    result = parse_measurement(input)
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO requests_log (timestamp, input_string, output_data) VALUES (%s, %s, %s)"
    values = (time.strftime('%Y-%m-%d %H:%M:%S'), input, str(result))
    
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"input": input, "result": result}

@app.get("/history")
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM requests_log")
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return rows

# Run Uvicorn on 0.0.0.0:8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_app:app", host="0.0.0.0", port=8080)
