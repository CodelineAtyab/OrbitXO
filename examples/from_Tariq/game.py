import uuid
import uvicorn
import fastapi

boards = {}

def create_uuid():
    return str(uuid.uuid4())

def create_board(board_id):
    boards[board_id] = [["", "", ""], ["", "", ""], ["", "", ""]]
    return boards[board_id]

app = fastapi.FastAPI()
@app.post("/board")
def create_board_endpoint():
    board_uuid = create_uuid()
    board = create_board(board_uuid)
    return {"board_id": board_uuid}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)