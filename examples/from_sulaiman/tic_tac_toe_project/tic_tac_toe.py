from fastapi import FastAPI
import uvicorn
import uuid
import utils

app = FastAPI()
@app.post("/board")
def create_board():
    board_id = str(uuid.uuid4())
    utils.tictactoe_games[board_id] = utils.empty_board()
    return {"board_id": board_id}

@app.get("/board/{board_id}")
def get_board(board_id: str):
    return utils.display_board(board_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8567)
