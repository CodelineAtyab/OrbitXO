
from fastapi import FastAPI
import uvicorn
import uuid  

app = FastAPI()

boards = {}

def generate_board_id():
    return str(uuid.uuid4())


def create_new_board(board_id):
    boards[board_id] = [["", "", ""], 
                        ["", "", ""], 
                        ["", "", ""]]
    
    return boards[board_id]

@app.post("/board")
def create_board():
    board_id = generate_board_id()
    create_new_board(board_id)
    return {"id_board": board_id}

@app.get("/board/{board_id}")
def get_board(board_id: str):
    if board_id not in boards:
        return {"error": "Board not found"}
    return {"board": boards[board_id]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)
