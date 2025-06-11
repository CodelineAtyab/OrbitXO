from fastapi import FastAPI
import uuid
import uvicorn
import util



app = FastAPI()

@app.post("/board")
def create_board():
    board_id = str(uuid.uuid4())

    util.games[board_id] = {
        "board": util.board(),
        "active_player": "X"
    }
    return {"board_id": board_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)