import sys
from fastapi import FastAPI, Query
from .converter import convert_measurements
from .crud import create_history, get_history
from .database import init_db
from .logger import logger

app = FastAPI(title="Package Measurement Conversion API")

# to initialize SQLite database
init_db()

@app.get("/convert-measurements")
def convert_api(input: str = Query(...)):
    result = convert_measurements(input)
    create_history(input, result)
    logger.info(f"Converted: {input} -> {result}")
    return result

@app.get("/history")
def history_api():
    rows = get_history()
    return rows

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=False)
