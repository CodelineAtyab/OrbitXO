import logging, os
from fastapi import FastAPI, Query
from converter import convert_measurements
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔹 Logging setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

app = FastAPI()

# 🔹 Database setup
DATABASE_URL = "mysql+pymysql://user:password@db:3306/measurements"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    input_str = Column(String(255))
    output_str = Column(String(255))

Base.metadata.create_all(bind=engine)

@app.get("/convert-measurements")
def convert_measurements_endpoint(input: str = Query(...)):
    result = convert_measurements(input)

    # Save to DB
    db = SessionLocal()
    entry = History(input_str=input, output_str=str(result))
    db.add(entry)
    db.commit()
    db.close()

    # Log
    logging.info(f"New request: input={input}, output={result}")
    return result

@app.get("/history")
def get_history():
    db = SessionLocal()
    records = db.query(History).all()
    db.close()
    return [{"id": r.id, "input": r.input_str, "output": r.output_str} for r in records]
