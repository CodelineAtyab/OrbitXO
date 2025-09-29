import uvicorn
from fastapi import FastAPI, Query
from decoder import decode_string
from db import save_history, get_history
import logging

app = FastAPI(title="Alphabet Alchemist API")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/app.log"),
        logging.StreamHandler()
    ]
)

@app.get("/convert-measurements")
def convert_measurements(input: str = Query(..., alias="input")):
    logging.info(f"Received input: {input}")
    result = decode_string(input)
    save_history(input, result)
    logging.info(f"Result: {result}")
    return result

@app.get("/history")
def history():
    return get_history()

if __name__ == "__main__":
    import sys
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    uvicorn.run("main_app:app", host="0.0.0.0", port=port, reload=False)
