
from fastapi import FastAPI
import uuid
import uvicorn

app = FastAPI()

game = {}

@app.post("/board")

def createBoard():
    board_id = str(uuid.uuid4())
    board = [["" for _ in range(3)] for _ in range(3)]
    game[board_id] = {"board": board, "active player": "X"}

    return {"board_id": board_id}

if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8888)



