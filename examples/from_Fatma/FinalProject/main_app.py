import time
import mysql.connector
from fastapi import FastAPI
from parser import parse_measurement
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Wait for MySQL to be ready
db_ready = False
while not db_ready:
    try:
        conn = mysql.connector.connect(
            host="mysql-db",
            user="user",
            password="password",
            database="measurements_db"
        )
        conn.close()
        db_ready = True
        print("✅ MySQL is ready!")
    except mysql.connector.Error:
        print("⏳ Waiting for MySQL...")
        time.sleep(2)

# FastAPI setup
app = FastAPI()

DATABASE_URL = "mysql+mysqlconnector://user:password@mysql-db:3306/measurements_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    input_str = Column(String(255))
    result = Column(String(255))

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/convert-measurements")
def convert_measurements(input: str):
    result = parse_measurement(input)
    db = SessionLocal()
    history_entry = History(input_str=input, result=str(result))
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    db.close()
    return {"input": input, "result": result}

@app.get("/history")
def get_history():
    db = SessionLocal()
    rows = db.query(History).all()
    db.close()
    return [{"id": r.id, "input": r.input_str, "result": r.result} for r in rows]

# Run Uvicorn on 0.0.0.0:8080
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_app:app", host="0.0.0.0", port=8080)
