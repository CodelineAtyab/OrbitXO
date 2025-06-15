from fastapi import FastAPI
import uvicorn
import uuid
import utils

app = FastAPI()
@app.post("/board")
def create_board():
    board_id = str(uuid.uuid4())
    utils.tictactoe_games[board_id] = {"board": utils.empty_board()
                                        , "player_turn": "1"
                                        , "player_1_symbol": "X"
                                        , "player_2_symbol": "O"
                                        , "game_over": False}
    return {"board_id": board_id}

@app.get("/boards")
def get_boards():
    return utils.display_boards()

@app.get("/board/{board_id}")
def get_board(board_id: str):
    return utils.display_board(board_id)

@app.post("/board/{board_id}/move")
def turn_tracker(board_id):
    return utils.turn_tracker(board_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8567)