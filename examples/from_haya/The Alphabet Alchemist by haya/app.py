from flask import Flask, request, jsonify, send_file
from converter import convert_measurements
import logging
import os
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import io

app = Flask(__name__)

# Configure logging
LOG_DIR = os.environ.get("LOG_DIR", "./logs")
os.makedirs(LOG_DIR, exist_ok=True)
log_file_path = os.path.join(LOG_DIR, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(log_file_path),
        logging.StreamHandler(sys.stdout)
    ]
)

# Database setup with retry
def setup_database():
    """Setup database connection with retry logic"""
    try:
        DATABASE_URL = os.environ.get("DATABASE_URL", "mysql+pymysql://user:password@db/aiops_db")
        engine = create_engine(DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            
        Session = sessionmaker(bind=engine)
        app.logger.info(f"Database connected successfully at {DATABASE_URL}")
        return engine, Session
    except Exception as e:
        app.logger.error(f"Database connection failed: {e}")
        return None, None

# Initialize database
engine, Session = setup_database()
Base = declarative_base()

class History(Base):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True)
    input_string = Column(String(255), nullable=False)
    output_result = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<History(input_string='{self.input_string}', output_result='{self.output_result}')>"

# Create tables if engine exists
if engine:
    Base.metadata.create_all(engine)

@app.route("/", methods=["GET"])
def home():
    """API documentation endpoint"""
    return jsonify({
        "name": "Package Measurement Converter API",
        "version": "1.0.0",
        "endpoints": {
            "/": "GET - API documentation",
            "/convert-measurements": "GET - Convert string to numbers (param: input)",
            "/history": "GET - Retrieve conversion history"
        }
    }), 200

@app.route("/convert-measurements", methods=["GET"])
def convert_measurements_endpoint():
    input_string = request.args.get("input")
    if not input_string:
        return jsonify({"error": "Missing 'input' parameter"}), 400

    try:
        result = convert_measurements(input_string)
        
        # Create JSON content in memory
        output_data = {"input": input_string, "output": result}
        json_str = json.dumps(output_data, indent=2)
        json_bytes = io.BytesIO(json_str.encode('utf-8'))
        
        # Store in history if database is available
        if Session:
            try:
                session = Session()
                history_entry = History(
                    input_string=input_string,
                    output_result=json_str
                )
                session.add(history_entry)
                session.commit()
            except SQLAlchemyError as e:
                app.logger.error(f"Database error: {e}")
            finally:
                session.close()
        
        # Prepare file for download
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output_{input_string}_{timestamp_str}.json"
        
        return send_file(
            json_bytes,
            as_attachment=True,
            download_name=filename,
            mimetype="application/json"
        )

    except Exception as e:
        app.logger.error(f"Conversion error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/history", methods=["GET"])
def get_history():
    session = Session()
    all_history = session.query(History).all()
    session.close()
    
    history_data = []
    for entry in all_history:
        history_data.append({
            "id": entry.id,
            "input_string": entry.input_string,
            "output_result": entry.output_result,
            "timestamp": entry.timestamp.isoformat()
        })
    app.logger.info("History endpoint called. Retrieved all history entries.")
    return jsonify(history_data), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            app.logger.error(f"Invalid port argument: {sys.argv[1]}. Using default port {port}.")
    
    app.logger.info(f"Starting Flask application on port {port}")
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_ENV") == "development")
