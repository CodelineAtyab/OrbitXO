from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
import random

# ✅ إعداد الاتصال بقاعدة البيانات
# لاحظ: كلمة السر فيها @ لذلك لازم تتحول لـ %40
DATABASE_URL = "mysql+pymysql://root:Arooba24%402000@localhost:3306/traffic_db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

# ✅ تعريف الجدول
class TravelTime(Base):
    __tablename__ = "travel_times"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String(100))
    destination = Column(String(100))
    travel_time = Column(Integer)

# ✅ دالة تسجيل وقت السفر
def record_travel_time(source: str, destination: str):
    db = SessionLocal()
    try:
        travel_time = random.randint(20, 40)  # رقم عشوائي للتجربة
        new_record = TravelTime(
            source=source,
            destination=destination,
            travel_time=travel_time,
            timestamp=datetime.utcnow()
        )
        db.add(new_record)
        db.commit()
        print(f"[INFO] Recorded travel time: {travel_time} minutes ({source} -> {destination}) at {datetime.utcnow()}")
    finally:
        db.close()

# ✅ دالة استرجاع البيانات من الجدول
def get_historical_data(source: str, destination: str, date: str):
    db = SessionLocal()
    try:
        results = db.query(TravelTime).filter(
            TravelTime.source == source,
            TravelTime.destination == destination,
            TravelTime.timestamp.like(f"{date}%")
        ).all()

        print(f"\n📊 Historical Data for {source} -> {destination} on {date}:")
        for row in results:
            print(f"{row.timestamp.strftime('%H:%M:%S')} - {row.travel_time} minutes")
        if not results:
            print("No data found for this date.")
    finally:
        db.close()

# ✅ جدولة التسجيل التلقائي كل 15 دقيقة
scheduler = BackgroundScheduler()
scheduler.add_job(record_travel_time, "interval", minutes=15, args=["home", "work"])
scheduler.start()

# ✅ تجربة مباشرة عند التشغيل
if __name__ == "__main__":
    # يسجل أول قراءة
    record_travel_time("home", "work")

    # يطبع البيانات التاريخية لليوم الحالي
    today = datetime.utcnow().strftime("%Y-%m-%d")
    get_historical_data("home", "work", today)




# ملاحظة: تأكد من تشغيل قاعدة البيانات MySQL قبل تشغيل هذا السكربت.
# in CMD ENTER "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -u root -p
# mysql> ENTER the code which in database.sql file to create database and table
# mysql> SELECT * FROM travel_times;                    # to see the data in the table
# mysql> SELECT COUNT(*) FROM travel_times;                  # to see how many rows in the table




