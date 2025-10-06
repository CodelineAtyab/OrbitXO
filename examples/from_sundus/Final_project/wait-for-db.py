#!/usr/bin/env python3
import time
import os
import sys
from sqlalchemy import create_engine
from main_app import app  # your FastAPI app

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("DATABASE_URL not set")
    sys.exit(1)

engine = create_engine(DATABASE_URL)

print("Waiting for MySQL to be ready...")

while True:
    try:
        with engine.connect():
            print("MySQL is available! Starting API...")
            break
    except Exception:
        print("MySQL is unavailable - sleeping for 3 seconds")
        time.sleep(3)

# Start FastAPI
import uvicorn

port = 8000
uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
