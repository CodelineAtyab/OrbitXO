from fastapi import FastAPI
import uvicorn

from board_id import create_new_board
from games_store import all_games  


app=FastAPI()


@app.post("/board")
def create_board():
    board_id = create_new_board()
    return {"board_id": board_id}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)