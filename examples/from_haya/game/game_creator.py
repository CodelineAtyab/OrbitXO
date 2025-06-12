from fastapi import FastAPI
from uuid import uuid1
import uvicorn

app=FastAPI()
board_state={}

@app.post("/board")
def board():
    board_id = uuid1()
    board_state[board_id] = {
        "board": [
           ["", "", ""],
           ["", "", ""],
           ["", "", ""]
        ],
    "active_player":"x"
    }
    return board_id

if __name__ =="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)