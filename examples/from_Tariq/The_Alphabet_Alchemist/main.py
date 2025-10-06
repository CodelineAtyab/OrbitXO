import uvicorn
from fastapi import FastAPI
from logsql import log_request_response  # For database logging
from log_config import api_logger         # For file logging

app = FastAPI(
    title="String Processor API",
    description="An API to process strings according to a specific set of rules.",
    version="1.0.0",
)

def string_to_number_list(s: str) -> list[int]:
    """
    Processes a string according to the defined rules and returns a list of numbers.
    Any character not in 'a'...'z' is treated as having a value of 0.
    """
    s = s.lower() # Convert input string to lowercase

    def get_char_value(char: str) -> int:
        """Helper function to get the value of a character."""
        if 'a' <= char <= 'z':
            return ord(char) - ord('a') + 1
        return 0

    result = []
    i = 0
    while i < len(s):
        # If a character's value is 0, it's a standalone sequence resulting in 0.
        if get_char_value(s[i]) == 0:
            result.append(0)
            i += 1
            continue

        # 1. Determine the count using the chained 'z' rule for counts
        count = 0
        while i < len(s) and s[i] == 'z':
            count += 26
            i += 1
        
        if i < len(s):
            count += get_char_value(s[i])
            i += 1
        
        # 2. Collect and sum characters based on the item rule
        sub_chars = []
        items_collected = 0
        
        while items_collected < count and i < len(s):
            # Check if the item is a z-chain
            if s[i] == 'z':
                # This is a z-chain item. Collect all z's and the char after.
                item_start_index = i
                while i < len(s) and s[i] == 'z':
                    i += 1
                if i < len(s): # Include the character that terminates the z-chain
                    i += 1
                sub_chars.extend(list(s[item_start_index:i]))
            else:
                # This is a single character item.
                sub_chars.append(s[i])
                i += 1
            
            items_collected += 1

        # 3. Sum and store the result
        current_sum = sum(get_char_value(c) for c in sub_chars)
        result.append(current_sum)
        
    return result

@app.get("/convert-measurements")
def process_string_endpoint(input: str):
    """
    Takes a string 's' as a query parameter, processes it, and logs the transaction.
    """
    output = string_to_number_list(input)
    response_data = {"input_string": input, "output": output}
    
    # Log to both the database and the file
    log_request_response(input, response_data)
    api_logger.info(f"Request processed: {response_data}")
    
    return response_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
