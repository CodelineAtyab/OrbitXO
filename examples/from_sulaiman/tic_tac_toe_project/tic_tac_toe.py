from fastapi import FastAPI
import uvicorn
import uuid
import utils

app = FastAPI()
@app.post("/board")
def create_board():
    board_id = str(uuid.uuid4())
    utils.tictactoe_games[board_id] = {
        "board": utils.board,
    }
    return {"board_id": board_id}
# @app.get("/board/{board_id}")

uvicorn.run(app, host="0.0.0.0", port=8567)