import uuid
import uvicorn
import fastapi
import utility as util



app = fastapi.FastAPI()
@app.post("/board")
def create_board_endpoint():
    board_uuid = util.create_uuid()
    board = util.create_board(board_uuid)
    return {"board_id": board_uuid}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)