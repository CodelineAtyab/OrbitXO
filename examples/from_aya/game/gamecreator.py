import uvicorn
from fastapi import FastAPI
import uuid

app = FastAPI()
boards = {}

@app.post("/board")
def create_board(): 
    board_id = str(uuid.uuid4()) 

    boards[board_id] = {
        "board": [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ],
    }
    return boards[board_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0" , port=8000) 

