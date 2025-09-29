from fastapi import FastAPI
from pydantic import BaseModel
try:
	from loguru import logger
except ImportError:
	import logging
	logger = logging.getLogger("measurement_converter")
	logging.basicConfig(level=logging.INFO)
import datetime
from typing import List
import os
import db_logger
import file_logger
try:
	import uvicorn
except Exception:
	uvicorn = None

def char_score(c: str) -> int:
	"""Return alphabetic score, a=1, b=2, ..., z=26, else 0."""
	return ord(c.lower()) - 96 if c.isalpha() else 0

from typing import Tuple
def z_special(input_str: str, idx: int) -> Tuple[int, int]:
	"""Handle z logic: z takes next char as its own, recursively."""
	score = char_score('z')
	next_idx = idx + 1
	if next_idx < len(input_str):
		next_char = input_str[next_idx]
		if next_char.lower() == 'z':
			nested_score, new_idx = z_special(input_str, next_idx)
			return score + nested_score, new_idx
		else:
			return score + char_score(next_char), next_idx + 1
	return score, next_idx

def measurement_converter(input_str: str) -> List[int]:
	"""
	Processes the string by segment, using the first char as count, summing next chars' scores.
	z is special: as counter or value, it absorbs the next char (recursively).
	"""
	logger.info(f"Converting: {input_str}")
	output = []
	idx = 0
	while idx < len(input_str):
		counter = input_str[idx]
		logger.debug(f"At idx {idx}, counter: {counter}")
		if counter.lower() == 'z':
			count, next_idx = z_special(input_str, idx)
			idx = next_idx
		else:
			count = char_score(counter)
			idx += 1
		if count == 0:
			output.append(0)
			continue
		segment_sum = 0
		to_process = count
		while to_process > 0 and idx < len(input_str):
			val_char = input_str[idx]
			if val_char.lower() == 'z':
				zval, next_idx = z_special(input_str, idx)
				segment_sum += zval
				idx = next_idx
			else:
				segment_sum += char_score(val_char)
				idx += 1
			to_process -= 1
		output.append(segment_sum)
	logger.info(f"Converted result: {output}")
	return output

# --- FastAPI Setup ---
app = FastAPI()

class MeasurementRequest(BaseModel):
	input_str: str


@app.on_event("startup")
async def on_startup():
	# Initialize DB connection (reads env vars DB_HOST/DB_PORT/DB_USER/DB_PASSWORD/DB_NAME)
	db_logger.init_db()
	try:
		file_logger.init_file_logger()
	except Exception:
		logger.exception("Failed to initialize file logger")


@app.on_event("shutdown")
async def on_shutdown():
	db_logger.close_db()
	# nothing to close for file_logger


@app.get("/measurement-convert", response_model=dict)
async def convert_get_endpoint(input_str: str):
	result = measurement_converter(input_str)
	try:
		db_logger.save_interaction(input_str, result)
		file_logger.save_log(input_str, result)
	except Exception:
		logger.exception("Failed to save interaction to DB and/or file")
	return {"input_str": input_str, "result": result}


@app.post("/measurement-convert", response_model=dict)
async def convert_post_endpoint(request: MeasurementRequest):
	result = measurement_converter(request.input_str)
	try:
		db_logger.save_interaction(request.input_str, result)
		file_logger.save_log(request.input_str, result)
	except Exception:
		logger.exception("Failed to save interaction to DB and/or file")
	return {"input_str": request.input_str, "result": result}

if __name__ == "__main__":
	if uvicorn is not None:
		print("Starting FastAPI app with uvicorn on 0.0.0.0:8080")
		uvicorn.run(app, host="0.0.0.0", port=8080)
	else:
		print("uvicorn is not installed. To run the server install uvicorn and try again:")
		print("    pip install uvicorn[standard]")