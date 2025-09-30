from fastapi import FastAPI, Query, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
import uvicorn
import logging

from Alphabet_Alchemist_func import convert_measurements
from db import init_db, insert_history, fetch_history




app = FastAPI(title="Alphabet Alchemist API")


# Logging setup
logging.basicConfig(
    filename="logs/app.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)



# Initialize DB when app starts
@app.on_event("startup")
def startup_event():
    init_db()
    logging.info("Database initialized.")


@app.get("/convert-measurements", response_model=List[int])
def convert_measurements_api(input: str = Query(..., description="Encoded input string")):
    """
    Convert input string into list of measured inflows.
    Example: GET /convert-measurements?input=abbcc → [2, 6]
    """
    try:
        result = convert_measurements(input)

        # Save to DB
        insert_history(input, result)

        logging.info(f"Input: {input} → Output: {result}")
        return JSONResponse(content=result, status_code=200)
    except Exception as e:
        logging.error(f"Error converting input '{input}': {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/history")
def get_history():
    """
    Fetch history of all previous conversions.
    Returns list of {id, input, output}.
    """
    try:
        rows = fetch_history()
        history_list = [{"id": r[0], "input": r[1], "output": r[2]} for r in rows]
        logging.info(f"add to the history fetched {len(history_list)} records.")
        return JSONResponse(content=history_list, status_code=200)
    
    except Exception as e:
        logging.error(f"Error fetching history: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

if __name__ == "__main__":
    uvicorn.run("main_app:app", host="0.0.0.0", port=8888)

