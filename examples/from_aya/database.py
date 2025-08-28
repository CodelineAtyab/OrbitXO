import os
import time
import logging
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from dateutil import parser as dateparser
import pytz

# ================== Load environment variables ==================
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "traffic_db")
LOCAL_TZ = os.getenv("LOCAL_TZ", "Asia/Muscat")

# Connection pooling options
POOL_SIZE = int(os.getenv("DB_POOL_SIZE", 5))
MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", 10))
POOL_RECYCLE = int(os.getenv("DB_POOL_RECYCLE", 1800))

# ================== Logging ==================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(filename)s] %(message)s"
)

# ================== Database ==================
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=POOL_SIZE,
    max_overflow=MAX_OVERFLOW,
    pool_recycle=POOL_RECYCLE,
    echo=False
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TravelTimeEstimate(Base):
    __tablename__ = "travel_time_estimates"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_utc = Column(DateTime, nullable=False)
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    minutes = Column(Integer, nullable=False)

def init_db():
    Base.metadata.create_all(engine)
    logging.info("[INFO] Connected to database")

# ================== Business logic ==================
def record_travel_time(source: str, destination: str, minutes: int, ts: datetime = None):
    session = SessionLocal()
    try:
        if ts is None:
            ts = datetime.now(timezone.utc)
        rec = TravelTimeEstimate(ts_utc=ts, source=source, destination=destination, minutes=minutes)
        session.add(rec)
        session.commit()
        logging.info(f"[INFO] Recorded travel time: {minutes} minutes ({source} -> {destination}) at {ts}")
    finally:
        session.close()
        logging.info("[INFO] Database connection closed")

def get_historical_data(source: str, destination: str, date_str: str):
    session = SessionLocal()
    try:
        # parse date in local timezone
        tz = pytz.timezone(LOCAL_TZ)
        start_local = tz.localize(dateparser.parse(date_str))
        end_local = start_local + timedelta(days=1)
        # convert to UTC
        start_utc = start_local.astimezone(pytz.UTC)
        end_utc = end_local.astimezone(pytz.UTC)

        results = session.query(TravelTimeEstimate).filter(
            TravelTimeEstimate.source == source,
            TravelTimeEstimate.destination == destination,
            TravelTimeEstimate.ts_utc >= start_utc,
            TravelTimeEstimate.ts_utc < end_utc
        ).order_by(TravelTimeEstimate.ts_utc.asc()).all()

        if not results:
            print(f"Date: {date_str}\nNo records found.")
            return

        print(f"Date: {date_str}")
        for r in results:
            local_ts = r.ts_utc.replace(tzinfo=timezone.utc).astimezone(tz)
            print(f"{local_ts.strftime('%H:%M:%S')} - {r.minutes} minutes")
    finally:
        session.close()

def get_current_travel_time_minutes(source: str, destination: str) -> int:
    """ Placeholder: replace with API call if needed """
    return 25  # fake value for demo

def scheduled_job(source: str, destination: str):
    minutes = get_current_travel_time_minutes(source, destination)
    record_travel_time(source, destination, minutes)

def run_scheduler(source: str, destination: str):
    scheduler = BackgroundScheduler()
    scheduler.add_job(lambda: scheduled_job(source, destination), "cron", minute="0,15,30,45")
    scheduler.start()
    logging.info("Scheduler started. Recording every 15 minutes... (Ctrl+C to stop)")
    try:
        while True:
            time.sleep(10)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        logging.info("Scheduler stopped.")

# ================== CLI ==================
def main():
    parser = argparse.ArgumentParser(description="Travel Time Recorder")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init-db", help="Initialize database tables")

    rec = sub.add_parser("record-once", help="Record one travel time entry")
    rec.add_argument("--source", required=True)
    rec.add_argument("--destination", required=True)
    rec.add_argument("--minutes", required=True, type=int)
    rec.add_argument("--ts", help="Timestamp, e.g., '2025-08-27 09:30:00'")

    hist = sub.add_parser("history", help="Get historical data")
    hist.add_argument("--source", required=True)
    hist.add_argument("--destination", required=True)
    hist.add_argument("--date", required=True)

    sched = sub.add_parser("run-scheduler", help="Run scheduler every 15 minutes")
    sched.add_argument("--source", required=True)
    sched.add_argument("--destination", required=True)

    args = parser.parse_args()

    if args.command == "init-db":
        init_db()
    elif args.command == "record-once":
        ts = dateparser.parse(args.ts) if args.ts else None
        record_travel_time(args.source, args.destination, args.minutes, ts)
    elif args.command == "history":
        get_historical_data(args.source, args.destination, args.date)
    elif args.command == "run-scheduler":
        run_scheduler(args.source, args.destination)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()