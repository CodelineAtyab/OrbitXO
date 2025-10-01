from typing import List, Dict, Any, Tuple
import uvicorn
from fastapi import FastAPI
from logsql import log_request_response
from log_config import api_logger

app = FastAPI(
    title="String Processor API",
    description="An API to process strings according to a specific set of rules.",
    version="1.0.0",
)

def _get_char_num_lower(char: str) -> int:
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 1
    return 0

def char_num(ch: str) -> int:
    if not ch:
        return 0
    return _get_char_num_lower(ch.lower())

def _read_count(s: str, i: int) -> Tuple[int, int]:
    count = 0
    while i < len(s) and s[i] == 'z':
        count += 26
        i += 1
    if i < len(s):
        count += _get_char_num_lower(s[i])
        i += 1
    return count, i

def _read_item(s: str, i: int) -> Tuple[str, int]:
    if i >= len(s):
        return "", i

    if s[i] != 'z':
        return s[i], i + 1

    item_start_index = i
    while i < len(s) and s[i] == 'z':
        i += 1
    if i < len(s):
        i += 1
    return s[item_start_index:i], i

def string_to_num_list(s: str) -> List[int]:
    s = s.lower()
    result: List[int] = []
    i = 0
    while i < len(s):
        if _get_char_num_lower(s[i]) == 0:
            result.append(0)
            i += 1
            continue

        count, i = _read_count(s, i)

        sub_chars: List[str] = []
        for _ in range(count):
            if i >= len(s):
                break
            item_str, i = _read_item(s, i)
            sub_chars.extend(list(item_str))

        current_sum = sum(_get_char_num_lower(c) for c in sub_chars)
        result.append(current_sum)

    return result

@app.get("/convert-measurements")
def convert_measurements_endpoint(input: str):
    output = string_to_num_list(input)
    response_data = {"input_string": input, "output": output}

    log_request_response(input, response_data)
    api_logger.info(f"Request processed: {response_data}")

    return response_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)