import time
import re
import os
import pymysql
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), 'app_service.log')
DB_HOST = os.getenv('DB_HOST', '127.0.0.1')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_USER = os.getenv('DB_USER', 'aiops')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'aiopspass')
DB_NAME = os.getenv('DB_NAME', 'ai_ops_db')

REQUEST_RE = re.compile(r"HTTP_REQUEST id=(?P<id>[a-f0-9\-]+) method=(?P<method>\w+) path=(?P<path>[^ ]+) body=(?P<body>.*)")
RESPONSE_RE = re.compile(r"HTTP_RESPONSE id=(?P<id>[a-f0-9\-]+) method=(?P<method>\w+) path=(?P<path>[^ ]+) status=(?P<status>\d+)(?: response=(?P<response>.*))?")


def connect_db():
    return pymysql.connect(host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def tail_log(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Go to end of file
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            yield line.strip()


def main():
    pending = {}
    conn = None
    while True:
        try:
            if conn is None:
                conn = connect_db()
            for line in tail_log(LOG_PATH):
                req_m = REQUEST_RE.search(line)
                if req_m:
                    data = req_m.groupdict()
                    pending[data['id']] = {
                        'method': data['method'],
                        'path': data['path'],
                        'body': data['body'],
                        'timestamp': datetime.utcnow(),
                    }
                    continue
                resp_m = RESPONSE_RE.search(line)
                if resp_m:
                    data = resp_m.groupdict()
                    rid = data['id']
                    status = int(data['status'])
                    if rid in pending:
                        rec = pending.pop(rid)
                        # insert into DB with optional response body
                        resp_row = data.get('response')
                        with conn.cursor() as cur:
                            cur.execute(
                                "INSERT INTO interactions (request_id, method, path, request_body, response_body, status, created_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
                                (
                                    rid,
                                    rec['method'],
                                    rec['path'],
                                    rec['body'],
                                    resp_row if resp_row is not None else None,
                                    status,
                                    rec['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                                )
                            )
                            conn.commit()
                    continue
        except pymysql.MySQLError as e:
            print(f"MySQL error: {e}. Reconnecting in 3s")
            try:
                if conn:
                    conn.close()
            except Exception:
                pass
            conn = None
            time.sleep(3)
        except FileNotFoundError:
            print(f"Log file {LOG_PATH} not found. Waiting...")
            time.sleep(2)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(2)


if __name__ == '__main__':
    main()
