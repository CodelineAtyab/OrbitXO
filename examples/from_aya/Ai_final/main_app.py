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
DATABASE_URL = "mysql+pymysql://aiops:aiopspass@mysql:3306/ai_ops_db"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    input_str = Column(String(255))
    output_str = Column(String(255))

# ✅ إنشاء الجداول عند بدء التطبيق
@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("✅ Database tables ensured at startup.")
    except Exception as e:
        logging.error(f"❌ Error creating tables: {e}")

@app.get("/convert-measurements")
def convert_measurements_endpoint(input: str = Query(...)):
    result = convert_measurements(input)

    db = SessionLocal()
    try:
        entry = History(input_str=input, output_str=str(result))
        db.add(entry)
        db.commit()
        logging.info(f"New request saved: input={input}, output={result}")
    except Exception as e:
        logging.error(f"❌ Error saving to DB: {e}")
    finally:
        db.close()

    return {"input": input, "output": result}

@app.get("/history")
def get_history():
    db = SessionLocal()
    try:
        records = db.query(History).all()
        return [{"id": r.id, "input": r.input_str, "output": r.output_str} for r in records]
    except Exception as e:
        logging.error(f"❌ Error fetching history: {e}")
        return []
    finally:
        db.close()
