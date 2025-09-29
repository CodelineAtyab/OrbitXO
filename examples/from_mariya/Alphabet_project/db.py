import mysql.connector
import json

def get_connection():
    return mysql.connector.connect(
        host="db",  # يربط مع اسم الخدمة داخل docker-compose
        user="root",
        password="root",
        database="measurements",
        port=3306   # داخل الحاوية يظل 3306 طبيعي
    )

def save_history(input_str, result):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            input VARCHAR(255) NOT NULL,
            result TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )""")
        cursor.execute("INSERT INTO history (input, result) VALUES (%s, %s)",
                       (input_str, json.dumps(result)))
        conn.commit()
        cursor.close()
        conn.close()
        print(f"✅ Data saved to MySQL: {input_str} -> {result}")
    except Exception as e:
        print(f"❌ Database error: {e}")

def get_history():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM history")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"❌ Database error: {e}")
        return []
