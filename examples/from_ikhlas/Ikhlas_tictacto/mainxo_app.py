import fastapi
import uvicorn
import utility_xo as util

app=fastapi.FastAPI()
@app.post("/board") # create new board

def create_board():
    board_uuid= util.uuid_create()
    util.board_creation(board_uuid)
    return {"board_id": board_uuid}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)