import uvicorn
from fastapi import FastAPI
from logsql import log_request_response  # For database logging
from log_config import api_logger         # For file logging


def _get_character_value(character: str) -> int:
    """Helper function to get the value of a character."""
    if 'a' <= character <= 'z':
        return ord(character) - ord('a') + 1
    return 0


def _parse_count_from_string(input_string: str, start_index: int) -> tuple[int, int]:
    """
    Process the count sequence using the chained 'z' rule.
    Returns (count, next_index).
    """
    current_index = start_index
    count = 0

    # First, count the number of 'z' characters from the start index.
    z_end_index = current_index
    while z_end_index < len(input_string) and input_string[z_end_index] == 'z':
        z_end_index += 1
    
    z_count = z_end_index - current_index
    count += z_count * 26
    current_index = z_end_index

    # Then, process the character that follows the 'z' sequence.
    if current_index < len(input_string):
        count += _get_character_value(input_string[current_index])
        current_index += 1
    
    return count, current_index


def _collect_string_items(input_string: str, start_index: int, item_count: int) -> tuple[list[str], int]:
    """
    Collect and return items based on the item rule.
    Returns (sub_chars, next_index).
    """
    collected_chars = []
    current_index = start_index

    for _ in range(item_count):
        if current_index >= len(input_string):
            break  # Stop if we're at the end of the string

        # A single item is collected in each iteration of this loop.
        # An item can be a single character or a 'z'-chain.

        item_start_pos = current_index
        if input_string[item_start_pos] == 'z':
            # This is a z-chain item. Find its end.
            item_end_pos = item_start_pos
            while item_end_pos < len(input_string) and input_string[item_end_pos] == 'z':
                item_end_pos += 1
            if item_end_pos < len(input_string):  # Also include the terminating character
                item_end_pos += 1
            
            # Add all characters of the z-chain item
            collected_chars.extend(list(input_string[item_start_pos:item_end_pos]))
            current_index = item_end_pos
        else:
            # This is a single-character item.
            collected_chars.append(input_string[item_start_pos])
            current_index += 1

    return collected_chars, current_index


def convert_string_to_number_list(input_string: str) -> list[int]:
    """
    Processes a string according to the defined rules and returns a list of numbers.
    Any character not in 'a'...'z' is treated as having a value of 0.
    """
    input_string = input_string.lower() # Convert input string to lowercase
    number_list = []
    current_index = 0
    
    while current_index < len(input_string):
        # If a character's value is 0, it's a standalone sequence resulting in 0.
        if _get_character_value(input_string[current_index]) == 0:
            number_list.append(0)
            current_index += 1
            continue

        # 1. Determine the count using the chained 'z' rule for counts
        item_count, current_index = _parse_count_from_string(input_string, current_index)
        
        # 2. Collect and sum characters based on the item rule
        collected_items, current_index = _collect_string_items(input_string, current_index, item_count)

        # 3. Sum and store the result
        sum_of_items = sum(_get_character_value(c) for c in collected_items)
        number_list.append(sum_of_items)
        
    return number_list


def create_fastapi_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="String Processor API",
        description="An API to process strings according to a specific set of rules.",
        version="1.0.0",
    )
    
    @app.get("/convert-measurements")
    def process_string(input_str: str):
        processed_output = convert_string_to_number_list(input_str)
        response_data = {"input_string": input_str, "output": processed_output}
        log_request_response(input_str, response_data)
        api_logger.info(f"Request processed: {response_data}")
        
        return response_data
    
    return app


# Create the app instance
app = create_fastapi_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8585)
