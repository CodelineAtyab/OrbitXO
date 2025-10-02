from typing import List
import uvicorn
from fastapi import FastAPI
from logsql import log_request_response
from log_config import api_logger

app = FastAPI(
    title="String Processor API",
    description="An API to process strings according to a specific set of rules.",
    version="1.0.0",
)


def get_char_value(char: str) -> int:
    """Return the numeric value of a character."""
    if 'a' <= char <= 'z':
        return ord(char) - ord('a') + 1
    else:
        return 0

def decode_cipher(encoded_string: str) -> List[int]:
    """Decode the cipher string according to the rules."""
    result = []
    i = 0
    
    while i < len(encoded_string):
        counter_value = 0
        
        if encoded_string[i] == 'z':
            while i < len(encoded_string) and encoded_string[i] == 'z':
                counter_value += 26
                i += 1
            
            if i < len(encoded_string):
                counter_value += get_char_value(encoded_string[i])
                i += 1
            else:
                break
        else:
            counter_value = get_char_value(encoded_string[i])
            i += 1
        
        if i >= len(encoded_string):
            break
        
        total_sum = 0
        values_read = 0
        
        while values_read < counter_value and i < len(encoded_string):
            current_value = 0
            
            if encoded_string[i] == 'z':
                while i < len(encoded_string) and encoded_string[i] == 'z':
                    current_value += 26
                    i += 1
                
                if i < len(encoded_string):
                    current_value += get_char_value(encoded_string[i])
                    i += 1
            else:
                current_value = get_char_value(encoded_string[i])
                i += 1
            
            total_sum += current_value
            values_read += 1
        
        result.append(total_sum)
    
    return result

@app.get("/convert-measurements")
def convert_measurements_endpoint(input: str):
    output = decode_cipher(input)
    response_data = {"input_string": input, "output": output}

    log_request_response(input, response_data)
    api_logger.info(f"Request processed: {response_data}")

    return response_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)