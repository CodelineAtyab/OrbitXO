from flask import Flask, request, jsonify
from log import logger   # استدعاء اللوج من log.py
from converter import convert_measurements
from datetime import datetime
import os
import time

# SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError

app = Flask(__name__)

# 🔗 إعداد الاتصال بقاعدة البيانات (من متغيرات البيئة أو قيم افتراضية)
DB_USER = os.getenv("DB_USER", "aiops_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "aiops_pass")
DB_HOST = os.getenv("DB_HOST", "db")     # في docker-compose الخدمة اسمها db
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "aiops_db")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ⚡️ حاول الاتصال بقاعدة البيانات مع إعادة المحاولة
MAX_RETRIES = 10
for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL, echo=True, future=True)
        connection = engine.connect()
        connection.close()
        logger.info("✅ Database connection established successfully")
        break
    except OperationalError as e:
        logger.warning(f"⏳ Attempt {attempt+1}/{MAX_RETRIES} - DB not ready yet... retrying")
        time.sleep(5)
else:
    logger.error("❌ Could not connect to the database after several attempts")
    raise RuntimeError("Database not reachable")

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 📦 جدول العمليات
class Operation(Base):
    __tablename__ = "operations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    input_string = Column(String(255), nullable=False)
    output_result = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

# إنشاء الجدول لو مش موجود
Base.metadata.create_all(bind=engine)


# 🏠 الصفحة الرئيسية
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Package Measurement Converter API",
        "version": "2.0.0",
        "endpoints": {
            "/": "GET - API documentation",
            "/convert-measurements": "GET - Convert string to numbers (param: input)",
            "/history": "GET - Retrieve conversion history from MySQL"
        }
    }), 200


# 🔄 تحويل النصوص إلى أرقام وتخزين النتيجة في MySQL
@app.route("/convert-measurements", methods=["GET"])
def convert_measurements_endpoint():
    input_string = request.args.get("input")
    if not input_string:
        return jsonify({"error": "Missing 'input' parameter"}), 400

    try:
        # نفذ الخوارزمية
        result = convert_measurements(input_string)

        # ✨ سجل العملية في MySQL
        db = SessionLocal()
        new_op = Operation(input_string=input_string, output_result=str(result))
        db.add(new_op)
        db.commit()
        db.close()

        logger.info(f"Saved to DB => Input: {input_string}, Output: {result}")

        return jsonify({
            "input": input_string,
            "output": result
        }), 200

    except Exception as e:
        logger.error(f"Conversion error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# 📜 استرجاع التاريخ من MySQL
@app.route("/history", methods=["GET"])
def get_history():
    try:
        db = SessionLocal()
        records = db.query(Operation).all()
        db.close()

        history = [
            {
                "id": r.id,
                "input": r.input_string,
                "output": r.output_result,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for r in records
        ]
        return jsonify({"history": history}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🚀 Starting Flask application on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
