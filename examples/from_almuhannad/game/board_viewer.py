from fastapi import FastAPI
import uvicorn
import util



app = FastAPI()

@app.post("/board")
def create_board():
    board_id = util.board()
    return {"board_id": board_id}

@app.get("/board/{board_id}")
def get_board_end(board_id):
    board = util.get_board(board_id)
    return {"board": board}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)