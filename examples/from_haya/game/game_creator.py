from fastapi import FastAPI
from uuid import uuid4
import uvicorn

app=FastAPI()
board_state={}

@app.post("/board")
def board():
    board_id = uuid4()
    board_state[board_id] = {
        "board": [
           ["", "", ""],
           ["", "", ""],
           ["", "", ""]
        ],
    }
    return board_id

if __name__ =="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)