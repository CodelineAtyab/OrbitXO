from fastapi import FastAPI
import uvicorn
import uuid 
import util


app= FastAPI()
@app.post("/board")

def board():
      new_game_id = str(uuid.uuid4())
      new_game = {
        "board": util.board(),         
        "active_player": "X"           
    }

      util.board_games[new_game_id] = new_game

      return {"board_id": new_game_id}
        
       
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0" ,port=8888)
