# main_app.py
import sys
import json
import logging
from logging.handlers import TimedRotatingFileHandler
from typing import List
from fastapi import FastAPI, Query
from pydantic import BaseModel
from datetime import datetime
import os
import time
from sqlalchemy import Column, Integer, String, Text, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError

# ----- convert_measurements function -----
def convert_measurements(s: str):
    def letter_value(ch):
        if 'a' <= ch <= 'z':
            return ord(ch) - ord('a') + 1
        if 'A' <= ch <= 'Z':
            return ord(ch) - ord('A') + 1
        return 0

    def fused_value(s, i):
        total = 0
        while i < len(s):
            total += 26
            i += 1
            if i < len(s) and s[i].lower() != 'z':
                total += letter_value(s[i])
                return total, i + 1
        return total, i

    results = []
    i = 0
    while i < len(s):
        if s[i].lower() == 'z':
            count, i = fused_value(s, i)
        else:
            count = letter_value(s[i])
            i += 1

        if count == 0:
            results.append(0)
            continue

        total = 0
        taken = 0
        while taken < count and i < len(s):
            if s[i].lower() == 'z':
                val, i = fused_value(s, i)
                total += val
                taken += 1
            else:
                total += letter_value(s[i])
                i += 1
                taken += 1

        if total == 0:
            results.append(count)
        else:
            results.append(total)

    return results

# ----- Logging setup -----
log_dir = os.environ.get("LOG_DIR", "./logs")
os.makedirs(log_dir, exist_ok=True)
logger = logging.getLogger("measurement_api")
logger.setLevel(logging.INFO)
fh = TimedRotatingFileHandler(os.path.join(log_dir, "app.log"), when="D", interval=1, backupCount=7)
fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(fmt)
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setFormatter(fmt)
logger.addHandler(ch)

# ----- DB setup with retry -----
Base = declarative_base()
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./history.db"

engine = None
for attempt in range(20):
    try:
        engine = create_engine(
            DATABASE_URL,
            connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
        )
        conn = engine.connect()
        conn.close()
        logger.info("Database connected successfully!")
        break
    except OperationalError:
        logger.warning(f"MySQL not ready, retrying... ({attempt+1}/20)")
        time.sleep(3)
else:
    raise Exception("Could not connect to MySQL after 20 attempts")

SessionLocal = sessionmaker(bind=engine)

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    input_str = Column(String(1000))
    result_json = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

# ----- FastAPI app -----
app = FastAPI(title="Package Measurement Conversion API")

class ConvertResponse(BaseModel):
    input: str
    result: List[int]

@app.get("/convert-measurements", response_model=ConvertResponse)
def convert_endpoint(input: str = Query(..., alias="input")):
    logger.info(f"Received input: {input}")
    result = convert_measurements(input)
    db = SessionLocal()
    rec = History(input_str=input, result_json=json.dumps(result))
    db.add(rec)
    db.commit()
    db.close()
    logger.info(f"Result: {result}")
    return {"input": input, "result": result}

@app.get("/history")
def get_history(limit: int = 50):
    db = SessionLocal()
    rows = db.query(History).order_by(History.created_at.desc()).limit(limit).all()
    out = [{"id": r.id, "input": r.input_str, "result": json.loads(r.result_json), "created_at": r.created_at.isoformat()} for r in rows]
    db.close()
    return out

if __name__ == "__main__":
    import uvicorn
    port = 8000  # fixed to 8000 for Docker/Swagger
    if len(sys.argv) >= 2:
        try:
            port = int(sys.argv[1])
        except:
            pass
    logger.info(f"Starting server on 0.0.0.0:{port}")
    uvicorn.run("main_app:app", host="0.0.0.0", port=port, log_level="info")
