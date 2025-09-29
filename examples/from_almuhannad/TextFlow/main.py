import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import logging
from typing import List

from logsql import log_request_response
from log_config import setup_logger
from logic import string_to_number_list


class ConversionRequest(BaseModel):
    input_string: str

class ConversionResponse(BaseModel):
    input_string: str
    output: List[int]


app = FastAPI(
    title="TextFlow API",
    version="1.0.0",
)


def get_logger():
    
    return setup_logger()


@app.post("/convert-measurements", response_model=ConversionResponse)
def process_string_endpoint(
    request: ConversionRequest, 
    logger: logging.Logger = Depends(get_logger)
):
   
    input_str = request.input_string
    output = string_to_number_list(input_str)
    
    response_data = ConversionResponse(input_string=input_str, output=output)
    
    
    log_request_response(input_str, response_data.dict())
    logger.info(f"Request processed: {response_data.dict()}")
    
    return response_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
