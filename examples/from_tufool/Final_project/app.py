from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime
import pymysql, time
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -----------------------------
# DB Settings
# -----------------------------
DB_USER = "tufool"
DB_PASSWORD = "1234"
DB_HOST = "db"
DB_NAME = "measurements_db"
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

Base = declarative_base()
engine = None
SessionLocal = None

class ConversionHistory(Base):
    __tablename__ = "conversion_history"
    id = Column(Integer, primary_key=True, index=True)
    measurement = Column(String(255), index=True)
    result = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

# -----------------------------
# Conversion Function
# -----------------------------
def convert_measurements(s: str) -> List[int]:
    def letter_value(ch):
        if 'a' <= ch <= 'z':
            return ord(ch) - ord('a') + 1
        return 0

    def consume_z(i):
        z_count, n = 0, len(s)
        while i < n and s[i] == 'z':
            z_count += 1
            i += 1
        j = i
        while j < n and not ('a' <= s[j] <= 'z'):
            j += 1
        if j < n and 'a' <= s[j] <= 'z':
            val = 26 * z_count + letter_value(s[j])
            return val, j + 1
        else:
            return 26 * z_count, j

    i, n, result = 0, len(s), []
    while i < n:
        ch = s[i]
        if ch == 'z':
            count, i = consume_z(i)
        elif 'a' <= ch <= 'z':
            count = letter_value(ch)
            i += 1
        else:
            result.append(0)
            i += 1
            continue

        total, taken = 0, 0
        while taken < count and i < n:
            if s[i] == 'z':
                val, i = consume_z(i)
            else:
                val = letter_value(s[i])
                i += 1
            total += val
            taken += 1
        result.append(total)
    return result

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI()

class MeasurementRequest(BaseModel):
    measurement: str

@app.on_event("startup")
def startup_event():
    """Wait for DB and create schema."""
    global engine, SessionLocal
    max_retries, delay = 20, 3
    for attempt in range(1, max_retries + 1):
        try:
            print(f"?? Attempt {attempt}: connecting to MySQL...")
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
            conn.autocommit(True)
            cur = conn.cursor()
            cur.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
            cur.close()
            conn.close()
            # Init SQLAlchemy
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            Base.metadata.create_all(bind=engine)
            print("? Database and tables ready.")
            return
        except Exception as e:
            print(f"? DB not ready ({e}), retrying in {delay}s...")
            time.sleep(delay)
    raise RuntimeError("? Could not connect to DB after retries.")

@app.post("/convert")
def convert(req: MeasurementRequest):
    db = SessionLocal()
    result = convert_measurements(req.measurement)
    history = ConversionHistory(measurement=req.measurement, result=str(result))
    db.add(history)
    db.commit()
    db.refresh(history)
    db.close()
    return {"result": result}

@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(ConversionHistory).all()
    db.close()
    return [
        {"id": r.id, "measurement": r.measurement, "result": r.result, "created_at": r.created_at}
        for r in records
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8888, reload=True)
