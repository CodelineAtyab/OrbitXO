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
from starlette.responses import Response

# --- Database Configuration ---
# Use a distinct environment variable name and fall back to a local SQLite DB (sync driver).
DATABASE_URL = os.getenv("MY_DATABASE_URL", "sqlite:///./ai_ops.db")
Base = declarative_base()

# For a sync engine, ensure SQLite disables check_same_thread
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # For other backends, try to use a pymysql driver when aiomysql provided
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

# Ensure tables exist (guarded so failures during import won't crash unintentionally)
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    # Log the actual exception for diagnosis and continue; runtime will attempt again
    logger.exception("Could not create tables at import time; will rely on runtime migrations or DB availability.")
    pass

# --- Converter logic (adapted) ---

def get_char_value(char: str) -> int:
    """Return alphabetic value a=1..z=26, underscore or others -> 0."""
    if not char or not char.isalpha():
        return 0
    return ord(char.lower()) - ord("a") + 1


def get_z_value_iter(s: str, index: int):
    """Iteratively compute the value contributed by one or more chained 'z' characters.
    Each 'z' contributes 26 plus the value of the next non-z character (if present).
    Returns (value, next_index).
    """
    total = 0
    i = index
    while i < len(s) and s[i].lower() == "z":
        total += 26
        i += 1
        # If there's a following char that's not another 'z', add its value and consume it
        if i < len(s) and s[i].lower() != "z":
            total += get_char_value(s[i])
            i += 1
            break
    return total, i


def convert_measurements(input_str: str) -> List[int]:
    """Convert input string into list of segment sums using adapted rules.
    Differences from original: iterative z handling and underscores/invalid chars treated as 0.
    """
    logger.info(f"Processing: {input_str}")
    results: List[int] = []
    i = 0
    n = len(input_str)
    while i < n:
        count_char = input_str[i]
        logger.debug(f"Index {i} count_char '{count_char}'")
        if count_char.lower() == "z":
            count, i = get_z_value_iter(input_str, i)
            logger.debug(f"Z-counter resolved to {count}, next index {i}")
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

@app.middleware("http")
async def log_requests_middleware(request: Request, call_next):
    # Generate a unique id to correlate request/response
    request_id = str(uuid.uuid4())
    # Read body safely (may be empty)
    body_bytes = await request.body()
    try:
        body_text = body_bytes.decode("utf-8")
    except Exception:
        body_text = str(body_bytes)
    logger.info(f"HTTP_REQUEST id={request_id} method={request.method} path={request.url.path} body={body_text}")
    # Call the next handler and capture response (avoid consuming streaming bodies)
    response = await call_next(request)

    # Try to log a response body when easily available; do not exhaust streaming iterators
    try:
        resp_text = None
        if hasattr(response, "body") and response.body is not None:
            body_val = response.body
            resp_text = body_val if isinstance(body_val, (bytes, bytearray)) else str(body_val)
        elif hasattr(response, "body_bytes") and response.body_bytes is not None:
            bb = response.body_bytes
            resp_text = bb.decode("utf-8", errors="replace") if isinstance(bb, (bytes, bytearray)) else str(bb)
        else:
            resp_text = "<streaming or non-text response>"
    except Exception:
        resp_text = "<response body unavailable>"

    # Truncate if too large
    try:
        resp_text = resp_text if isinstance(resp_text, str) else str(resp_text)
        if len(resp_text) > 2000:
            resp_text = resp_text[:2000] + "...(truncated)"
    except Exception:
        resp_text = "<unable to decode response for logging>"

    logger.info(f"HTTP_RESPONSE id={request_id} method={request.method} path={request.url.path} status={response.status_code} response={resp_text}")
    # Return the original response (do not rebuild to preserve streaming behavior)
    return response

class ConvertRequest(BaseModel):
    input_str: str

def save_to_history_sync(input_str: str, result: List[int]):
    """Synchronous DB write using SQLAlchemy session."""
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

@app.get("/api/convert")
async def api_convert_get(input_str: str):
    """GET endpoint: returns conversion result; does not raise on DB save failure."""
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

    try:
        return await run_in_threadpool(fetch_history_sync)
    except Exception as e:
        logger.error(f"History fetch failed: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch history")

@app.get("/health")
async def health():
    return {"status": "ok", "time": datetime.datetime.utcnow().isoformat()}

@app.on_event("startup")
async def startup():
    logger.add("app_service.log", rotation="1 day", retention="7 days", level="INFO")
    # Attempt to create tables at runtime where filesystem permissions are likely correct
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ensured at startup.")
    except Exception:
        logger.exception("Failed to create database tables at startup")
    # No async database to connect for sync SQLAlchemy usage
    pass

@app.on_event("shutdown")
async def shutdown():
    # No async database to disconnect
    pass

if __name__ == "__main__":
    # Pass the app object directly to avoid importing the module twice when executed as a script
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", "8080")), reload=False)
