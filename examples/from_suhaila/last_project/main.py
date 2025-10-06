import os
import datetime
from loguru import logger
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from sqlalchemy import (
    create_engine, Column, Integer, String, JSON, DateTime
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from databases import Database

# -------------------- CONFIGURATION --------------------
DB_CONN_STR = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://user:password@localhost/dbname"
)

database = Database(DB_CONN_STR)

Base = declarative_base()
engine = create_engine(DB_CONN_STR.replace("aiomysql", "pymysql"))
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


# -------------------- DATABASE MODEL --------------------
class ConversionRecord(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    original_input = Column(String(255))
    output = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


Base.metadata.create_all(bind=engine)


# -------------------- LOGIC FUNCTIONS --------------------
def char_value(c: str) -> int:
    """Return numeric value of letter: a=1, b=2, ... z=26."""
    if c.isalpha():
        return ord(c.lower()) - ord("a") + 1
    return 0


def resolve_z_value(s: str, pos: int):
    """
    Handles 'z' logic:
    - 'z' as counter: 26 + next letter value
    - 'z' as value: adds next letter value recursively
    """
    val = char_value("z")
    next_pos = pos + 1

    if next_pos < len(s):
        nxt_char = s[next_pos]
        if nxt_char.lower() == "z":
            rec_val, final_pos = resolve_z_value(s, next_pos)
            return val + rec_val, final_pos
        return val + char_value(nxt_char), next_pos + 1

    return val, next_pos


def convert_measurements_logic(text: str):
    """
    Process string in segments:
    - First char = counter
    - Next counter chars = values to sum
    - Special rules for 'z'
    """
    logger.info(f"Starting conversion for: '{text}'")
    results = []
    idx = 0

    while idx < len(text):
        current_char = text[idx]
        logger.debug(f"Index {idx}, char '{current_char}'")
        segment_count = 0

        if current_char.lower() == "z":
            segment_count, idx = resolve_z_value(text, idx)
            logger.debug(f"Z-counter: count={segment_count}, idx={idx}")
        else:
            segment_count = char_value(current_char)
            idx += 1

        if segment_count == 0:
            logger.warning(f"Zero count for char '{current_char}' at index {idx - 1}")
            results.append(0)
            continue

        subtotal = 0
        chars_remaining = segment_count

        while chars_remaining > 0 and idx < len(text):
            val_char = text[idx]

            if val_char.lower() == "z":
                z_val, idx = resolve_z_value(text, idx)
                subtotal += z_val
                logger.debug(f"Z-value: {z_val}, idx={idx}")
            else:
                subtotal += char_value(val_char)
                logger.debug(f"Char '{val_char}' value: {char_value(val_char)}, subtotal={subtotal}")
                idx += 1

            chars_remaining -= 1

        logger.info(f"Segment result: {subtotal}")
        results.append(subtotal)

    logger.info(f"Conversion complete for '{text}': {results}")
    return results


# -------------------- API SETUP --------------------
app = FastAPI()


class ConversionInput(BaseModel):
    input_str: str


async def log_history(input_str: str, results: list):
    await database.execute(
        ConversionRecord.__table__.insert().values(
            original_input=input_str,
            output={"result": results},
            created_at=datetime.datetime.utcnow()
        )
    )


@app.get("/convert-measurements")
async def convert_get(input: str):
    logger.info(f"GET request received: {input}")
    results = convert_measurements_logic(input)
    await log_history(input, results)
    return results




@app.get("/history")
async def get_history():
    logger.info("Fetching history")
    return await database.fetch_all(ConversionRecord.__table__.select())


@app.on_event("startup")
async def startup_event():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_event():
    await database.disconnect()


# -------------------- LOGGER --------------------
logger.add("conversion.log", rotation="7 days", retention="14 days", level="INFO")


# -------------------- RUN SERVER --------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8070)
