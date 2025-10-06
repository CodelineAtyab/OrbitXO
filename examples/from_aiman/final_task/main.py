import uvicorn
from fastapi import FastAPI
from logsql import db_logger   
from log_config import api_logger         

app = FastAPI(
    title="String Processor Service",
    description="Provides an API endpoint for processing strings using predefined transformation rules.",
    version="1.0",
)




def string_to_number_list(text: str) -> list[int]:
    """
    Convert a string into a list of numbers based on custom rules:
    - Characters 'a'...'z' → mapped to 1...26
    - Any non-alphabet → 0
    - 'z'-chains determine counts or items
    """

    def char_value(c: str) -> int:
        """Return numeric value of a character, 0 if not a-z."""
        return ord(c) - ord("a") + 1 if "a" <= c <= "z" else 0

    result, i = [], 0
    text = text.lower()

    while i < len(text):
       
        if char_value(text[i]) == 0:
            result.append(0)
            i += 1
            continue

       
        count = 0
        while i < len(text) and text[i] == "z":
            count += 26
            i += 1
        if i < len(text):
            count += char_value(text[i])
            i += 1

        
        sub_chars, collected = [], 0
        while collected < count and i < len(text):
            if text[i] == "z":
                start = i
                while i < len(text) and text[i] == "z":
                    i += 1
                if i < len(text):
                    i += 1 
                sub_chars.extend(list(text[start:i]))
            else:
                sub_chars.append(text[i])
                i += 1
            collected += 1

        
        result.append(sum(char_value(c) for c in sub_chars))

    return result


@app.get("/convert-measurements")
def convert_measurements(input: str):
    """
    Process the input string, log the transaction, and return the result.
    """
    output = string_to_number_list(input)
    response = {"input_string": input, "output": output}

    
    db_logger.log_interaction(input, response)
    api_logger.info(f"Processed request: {response}")

    return response


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
