import fastapi
import uvicorn
import uuid

app = fastapi.FastAPI()

xo_board = {}

def unique_uuid():
    return str(uuid.uuid4())

def board_creation(id_board):
    xo_board[id_board] = {
        "board": [["", "", ""], ["", "", ""], ["", "", ""]],
        "active_player": 1 
    }
    return xo_board[id_board]

@app.post("/board")
def board_endpoint():
    uuid_board = unique_uuid()
    board_creation(uuid_board)
    return {"id_board": uuid_board}

@app.get("/board/{id_board}")
def get_board_endpoint(id_board: str):
    if id_board not in xo_board:
        return {"error": "Board not found"}
    return {"board": xo_board[id_board]["board"]}

@app.get("/board/{id_board}/move")
def get_active_player(id_board: str):
    if id_board not in xo_board:
        return {"error": "Board not found"}
    
    active_player = xo_board[id_board]["active_player"]
    symbol = "X" if active_player == 1 else "O"
    
    return {"player": active_player, "symbol": symbol}

@app.post("/board/{id_board}/move")
def make_move(id_board: str, row: int, col: int):
    if id_board not in xo_board:
        return {"error": "Board not found"}

    if not (0 <= row <= 2 and 0 <= col <= 2):
        return {"error": "Invalid position"}

    board = xo_board[id_board]["board"]
    player = xo_board[id_board]["active_player"]
    symbol = "X" if player == 1 else "O"

    if board[row][col] != "":
        return {"error": "Cell already filled"}

    board[row][col] = symbol

    xo_board[id_board]["active_player"] = 2 if player == 1 else 1      # Switching player

    return {
        "board": board,
        "next_player": xo_board[id_board]["active_player"],
        "next_symbol": "X" if xo_board[id_board]["active_player"] == 1 else "O"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888) 