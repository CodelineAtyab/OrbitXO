from loguru import logger
from fastapi import FastAPI, HTTPException, Request
import uuid
from pydantic import BaseModel
import uvicorn
import datetime
from sqlalchemy import create_engine, Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from typing import List
from starlette.concurrency import run_in_threadpool

# --- Database Configuration ---
DATABASE_URL = os.getenv("MY_DATABASE_URL", "sqlite:///./ai_ops.db")
Base = declarative_base()

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    sync_engine_url = DATABASE_URL.replace("+aiomysql", "")
    engine = create_engine(sync_engine_url.replace("aiomysql", "pymysql"))

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Database Model ---
class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    input_str = Column(String(255))
    result = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    logger.exception("Could not create tables at import time.")

# --- Converter logic ---
def get_char_value(char: str) -> int:
    if not char or not char.isalpha():
        return 0
    return ord(char.lower()) - ord("a") + 1

def get_z_value_iter(s: str, index: int):
    total = 0
    i = index
    while i < len(s) and s[i].lower() == "z":
        total += 26
        i += 1
        if i < len(s) and s[i].lower() != "z":
            total += get_char_value(s[i])
            i += 1
            break
    return total, i

def convert_measurements(input_str: str) -> List[int]:
    logger.info(f"Processing: {input_str}")
    results: List[int] = []
    i = 0
    n = len(input_str)
    while i < n:
        count_char = input_str[i]
        if count_char.lower() == "z":
            count, i = get_z_value_iter(input_str, i)
        else:
            count = get_char_value(count_char)
            i += 1
        if count == 0:
            results.append(0)
            continue
        seg_sum = 0
        to_take = count
        while to_take > 0 and i < n:
            ch = input_str[i]
            if ch.lower() == "z":
                val, new_i = get_z_value_iter(input_str, i)
                seg_sum += val
                i = new_i
            else:
                seg_sum += get_char_value(ch)
                i += 1
            to_take -= 1
        results.append(seg_sum)
    logger.info(f"Result for '{input_str}': {results}")
    return results

# --- FastAPI app ---
app = FastAPI()

class ConvertRequest(BaseModel):
    input_str: str

def save_to_history_sync(input_str: str, result: List[int]):
    session = SessionLocal()
    try:
        rec = History(input_str=input_str, result={"result": result}, timestamp=datetime.datetime.utcnow())
        session.add(rec)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.warning(f"Failed to save history (sync): {e}")
    finally:
        session.close()

# ✅ المسارات الجديدة (اللي جربتيها)
@app.get("/convert-measurements")
async def convert_get(input: str):
    res = convert_measurements(input)
    await run_in_threadpool(save_to_history_sync, input, res)
    return {"input_str": input, "result": res}

@app.get("/history")
async def history_get():
    def fetch_history_sync():
        session = SessionLocal()
        try:
            rows = session.query(History).all()
            return [
                {
                    "id": r.id,
                    "input_str": r.input_str,
                    "result": r.result,
                    "timestamp": r.timestamp.isoformat() if r.timestamp else None,
                }
                for r in rows
            ]
        finally:
            session.close()
    return await run_in_threadpool(fetch_history_sync)

# ✅ نخلي القديم يشتغل كمان (/api/convert, /api/history)
@app.get("/api/convert")
async def api_convert_get(input_str: str):
    res = convert_measurements(input_str)
    await run_in_threadpool(save_to_history_sync, input_str, res)
    return {"input_str": input_str, "result": res}

@app.post("/api/convert")
async def api_convert_post(req: ConvertRequest):
    res = convert_measurements(req.input_str)
    await run_in_threadpool(save_to_history_sync, req.input_str, res)
    return {"input_str": req.input_str, "result": res}

@app.get("/api/history")
async def api_history():
    return await history_get()

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.datetime.utcnow().isoformat()}

@app.on_event("startup")
async def startup():
    logger.add("app_service.log", rotation="1 day", retention="7 days", level="INFO")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ensured at startup.")
    except Exception:
        logger.exception("Failed to create database tables at startup")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")), reload=False)
