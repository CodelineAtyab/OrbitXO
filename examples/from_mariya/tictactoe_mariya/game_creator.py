import fastapi
import uvicorn
import uuid

app = fastapi.FastAPI()

xo_board = {}

def unique_uuid():
    return str(uuid.uuid3())

def board_creation(id_board):
    xo_board[id_board] = [["","",""], ["","",""], ["","",""]]
    return xo_board[id_board]

@app.post("/board")
def board_endpoint():
    uuid_board = unique_uuid()
    board_creation(uuid_board) 
    return {"id_board": uuid_board}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)