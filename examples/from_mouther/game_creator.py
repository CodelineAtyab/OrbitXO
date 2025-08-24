from fastapi import FastAPI
import uuid
import uvicorn

app = FastAPI()

# In-memory store for games
games = {}

@app.post("/board")
def create_board():
    board_id = str(uuid.uuid4())
    games[board_id] = {
        "board": [["" for _ in range(3)] for _ in range(3)],
        "active_player": "X"
    }
    return {"board_id": board_id}

if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8888)