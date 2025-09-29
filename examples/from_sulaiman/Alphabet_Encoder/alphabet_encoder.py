from fastapi import FastAPI
import uvicorn
from sql_logs import log_request, init_db

app = FastAPI()

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def convert_measurements(input: str):
    count_str = ""
    value_str = ""
    result = []
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    alphabet_dict = {letter: index + 1 for index, letter in enumerate(alphabet)}
    count = 0
    z_count = 0
    while count < len(input):
        if input[count] in alphabet_dict:
            while input[count] == "z":
                z_count+=1
                count+=1
            if input[count] in alphabet_dict:
                value_endpoint = count + alphabet_dict[input[count]] + (z_count*26)
            else:
                value_endpoint = count + 0 + (z_count*26)
            count+=1
            value = 0
            z_count = 0
            while count <= value_endpoint and count < len(input):
                if input[count] in alphabet_dict:
                    if input[count] == "z":
                        value_endpoint+=1
                    value += alphabet_dict[input[count]]
                count += 1
            result.append(value)
        else:
            result.append(0)
            count += 1
    # Create the output dictionary
    output = {"output": result}
    
    # Log the request to the database
    log_request(input, output)
    
    print(result)
    return output

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010)