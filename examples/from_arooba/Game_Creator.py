from fastapi import FastAPI
import uvicorn
import uuid 
import util


app= FastAPI()
@app.post("/board")

def board():
      new_game_id = str(uuid.uuid4())

    # Make a new board and set the starting player
      new_game = {
        "board": util.board(),         # Create a 3x3 empty board
        "active_player": "X"           # Set "X" as the player who starts
    }

    # Save the game in the board_games dictionary using the ID
      util.board_games[new_game_id] = new_game

    # Send back the game ID so the player can use it later
      return {"board_id": new_game_id}
        
       

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0" ,port=8888)
