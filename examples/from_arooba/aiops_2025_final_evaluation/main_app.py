from flask import Flask, request, jsonify
from log import logger   # استدعاء اللوج من log.py
from converter import convert_measurements
import os
import json
from datetime import datetime

app = Flask(__name__)

# 🏠 الصفحة الرئيسية
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "name": "Package Measurement Converter API",
        "version": "1.0.0",
        "endpoints": {
            "/": "GET - API documentation",
            "/convert-measurements": "GET - Convert string to numbers (param: input)",
            "/history": "GET - Retrieve conversion history"
        }
    }), 200


# 🔄 تحويل النصوص إلى أرقام
@app.route("/convert-measurements", methods=["GET"])
def convert_measurements_endpoint():
    input_string = request.args.get("input")
    if not input_string:
        return jsonify({"error": "Missing 'input' parameter"}), 400

    try:
        # نفذ الخوارزمية من converter.py
        result = convert_measurements(input_string)

        # ✨ سجل العملية في ملف اللوج
        logger.info(f"Operation => Input: {input_string}, Output: {result}")

        # (اختياري) احفظ النتيجة كملف JSON
        output_dir = os.environ.get("OUTPUT_DIR", "./outputs")
        os.makedirs(output_dir, exist_ok=True)
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(output_dir, f"output_{input_string}_{timestamp_str}.json")
        with open(filename, "w") as f:
            json.dump({"input": input_string, "output": result}, f, indent=2)

        return jsonify({
            "input": input_string,
            "output": result,
            "saved_to": filename
        }), 200

    except Exception as e:
        logger.error(f"Conversion error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


# 📜 استرجاع التاريخ (history) من اللوج
@app.route("/history", methods=["GET"])
def get_history():
    try:
        history_entries = []
        with open("logs/app.log", "r") as log_file:
            for line in log_file.readlines():
                if "Operation =>" in line:
                    history_entries.append(line.strip())
        return jsonify({"history": history_entries}), 200
    except FileNotFoundError:
        return jsonify({"error": "No history log found."}), 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"Starting Flask application on port {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
