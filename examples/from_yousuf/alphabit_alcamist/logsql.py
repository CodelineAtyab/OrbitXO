import os
import json
import time
import datetime
import mysql.connector
from mysql.connector import Error
from typing import Any, Dict

# Environment-driven configuration (defaults match original docker-compose values)
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "your_username")
DB_PASS = os.getenv("DB_PASS", "your_password")
DB_NAME = os.getenv("DB_NAME", "api_log_db")
DB_RETRIES = int(os.getenv("DB_RETRIES", "3"))
DB_RETRY_DELAY = float(os.getenv("DB_RETRY_DELAY", "1.0"))
FALLBACK_PATH = os.getenv("LOG_FALLBACK_DIR", ".")

def log_request_response(input_str: str, output_data: Dict[str, Any]) -> None:
    """
    Persist a request/response pair to the MySQL 'requests_log' table.
    On repeated database failures, write a JSON-line to a fallback file.
    """
    ts = datetime.datetime.utcnow().isoformat()
    payload_json = json.dumps(output_data, default=str, ensure_ascii=False)

    attempts = 0
    while attempts < DB_RETRIES:
        conn = None
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASS,
                database=DB_NAME,
            )
            cur = conn.cursor()
            sql = (
                "INSERT INTO requests_log (timestamp, input_string, output_data) "
                "VALUES (%s, %s, %s)"
            )
            cur.execute(sql, (ts, input_str, payload_json))
            conn.commit()
            try:
                cur.close()
            except Exception:
                pass
            return
        except Error as err:
            # Minimal diagnostic output; keep module lightweight
            print(f"MySQL logging failed (attempt {attempts + 1}/{DB_RETRIES}): {err}")
            attempts += 1
            time.sleep(DB_RETRY_DELAY)
        finally:
            if conn:
                try:
                    conn.close()
                except Exception:
                    pass

    # If we reach here, DB logging didn't succeed. Write to fallback JSONL.
    try:
        os.makedirs(FALLBACK_PATH, exist_ok=True)
        fallback_file = os.path.join(FALLBACK_PATH, "requests_log_fallback.jsonl")
        entry = {"timestamp": ts, "input": input_str, "output": output_data}
        with open(fallback_file, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, default=str, ensure_ascii=False) + "\n")
    except Exception as ex:
        # Last resort: print the unlogged entry so it isn't completely silent
        print(f"Fallback logging failed: {ex}")
        print("Unlogged entry:", {"timestamp": ts, "input": input_str, "output": output_data})