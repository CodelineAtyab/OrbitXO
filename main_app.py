"""
FastAPI Tic-Tac-Toe Game - Player vs Bot
Serves a colorful HTML interface and provides API endpoints for gameplay.
"""
import uuid
import os
import random
import time
import uvicorn

from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from prometheus_fastapi_instrumentator import Instrumentator

from app_logger import get_logger

# Initialize logger
logger = get_logger(os.path.basename(__file__))

app_version = "latest"
try:
    with open("version.txt") as version_file:
        app_version = version_file.read().strip()
        logger.info(f"Application version set to: {app_version}")
except FileNotFoundError:
    logger.error("Version file not found, using default version")
    pass

    
app = FastAPI(
    title="OrbitXO Tic-Tac-Toe API",
    description="A player vs bot tic-tac-toe game with colorful UI",
    version=app_version
)

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)

# Game storage - using simple dict for now (no DB needed)
games: Dict[str, Dict] = {}

# Default board ID for single game mode
DEFAULT_BOARD_ID = "main_game"

def create_new_board() -> List[str]:
    """Create a new empty tic-tac-toe board"""
    return ["", "", "", "", "", "", "", "", ""]

def check_winner(board: List[str], player: str) -> bool:
    """Check if a player has won the game"""
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for combo in win_combinations:
        if all(board[pos] == player for pos in combo):
            logger.debug(f"Winning combination for player {player}: {combo}")
            return True
    return False

def is_board_full(board: List[str]) -> bool:
    """Check if the board is full (draw condition)"""
    return all(cell != "" for cell in board)

def get_available_positions(board: List[str]) -> List[int]:
    """Get list of empty positions on the board"""
    return [i for i, cell in enumerate(board) if cell == ""]

def get_bot_move(board: List[str]) -> int:
    """Get bot's move (random for now)"""
    available = get_available_positions(board)
    if available:
        return random.choice(available)
    return -1

def initialize_game() -> Dict:
    """Initialize a new game state"""
    return {
        "board": create_new_board(),
        "current_player": "X",  # Player is X, Bot is O
        "game_status": "playing",  # playing, won, draw
        "winner": None,
        "created_at": time.time()
    }

# Initialize default game
games[DEFAULT_BOARD_ID] = initialize_game()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main game interface"""
    try:
        with open("index.html", "rb") as f:
            content = f.read()
            logger.info("Index page served successfully")
            logger.debug(f"Index page content size: {len(content)} bytes")
            return HTMLResponse(content=content, status_code=200)
    except FileNotFoundError:
        logger.error("Index page not found")
        return HTMLResponse(
            content="<h1>Game interface not found. Please ensure index.html exists.</h1>",
            status_code=404
        )


@app.get("/version")
async def get_version():
    """Get the current version of the application"""
    # logger.info(f"Version info returned: {app_version}", extra={"version": app_version})
    # Get a UUID in string format
    log_statement_id = str(uuid.uuid4())
    logger.error(f"[{log_statement_id}] Unable to get the version! File doesn't exist in /var/lib/jenkins", extra={"error_msg": app_version, "id": log_statement_id})
    # raise Exception("Unable to get the version! File doesn't exist in /var/lib/jenkins")
    return {"version": app_version}


@app.post("/board/player/{position}")
async def make_player_move(position: int):
    """
    Make a player move at the specified position (0-8)
    Bot will automatically respond if the game continues
    """
    if position < 0 or position > 8:
        logger.error(f"Invalid position attempted: {position}")
        raise HTTPException(status_code=400, detail="Position must be between 0 and 8")
    
    game = games[DEFAULT_BOARD_ID]
    
    if game["game_status"] != "playing":
        logger.error(f"Move attempted on finished game with status: {game['game_status']}")
        raise HTTPException(status_code=400, detail="Game is already finished")
    
    if game["current_player"] != "X":
        logger.error("Player attempted to move during bot's turn")
        raise HTTPException(status_code=400, detail="Not player's turn")
    
    if game["board"][position] != "":
        logger.error(f"Player attempted move on occupied position: {position}")
        raise HTTPException(status_code=400, detail="Position already occupied")
    
    # Make player move
    game["board"][position] = "X"
    logger.info(f"Player made move at position {position}")
    
    # Check if player won
    if check_winner(game["board"], "X"):
        game["game_status"] = "won"
        game["winner"] = "player"
        logger.info("Game ended: Player won")
        return {
            "board": game["board"],
            "game_status": game["game_status"],
            "winner": game["winner"],
            "message": "Player wins!"
        }
    
    # Check for draw
    if is_board_full(game["board"]):
        game["game_status"] = "draw"
        logger.info("Game ended: Draw after player move")
        return {
            "board": game["board"],
            "game_status": game["game_status"],
            "winner": None,
            "message": "It's a draw!"
        }
    
    # Bot's turn
    game["current_player"] = "O"
    bot_position = get_bot_move(game["board"])
    
    if bot_position != -1:
        game["board"][bot_position] = "O"
        logger.info(f"Bot made move at position {bot_position}")
        
        # Check if bot won
        if check_winner(game["board"], "O"):
            game["game_status"] = "won"
            game["winner"] = "bot"
            logger.info("Game ended: Bot won")
            return {
                "board": game["board"],
                "game_status": game["game_status"],
                "winner": game["winner"],
                "bot_move": bot_position,
                "message": "Bot wins!"
            }
        
        # Check for draw after bot move
        if is_board_full(game["board"]):
            game["game_status"] = "draw"
            logger.info("Game ended: Draw after bot move")
            return {
                "board": game["board"],
                "game_status": game["game_status"],
                "winner": None,
                "bot_move": bot_position,
                "message": "It's a draw!"
            }
    
    # Game continues
    game["current_player"] = "X"
    logger.info("Game continues - player's turn")
    return {
        "board": game["board"],
        "game_status": game["game_status"],
        "winner": game["winner"],
        "bot_move": bot_position,
        "message": "Your turn!"
    }


@app.get("/board/{board_id}")
async def get_board_state(board_id: str):
    """Get the current state of the specified board"""
    if board_id not in games:
        logger.error(f"Board not found: {board_id}")
        raise HTTPException(status_code=404, detail="Board not found")
    
    game = games[board_id]
    logger.info(f"Board state retrieved for board ID: {board_id}")
    return {
        "board_id": board_id,
        "board": game["board"],
        "current_player": game["current_player"],
        "game_status": game["game_status"],
        "winner": game["winner"]
    }


@app.post("/board/{board_id}/reset")
async def reset_board(board_id: str):
    """Reset the board to start a new game"""
    if board_id not in games:
        logger.error(f"Attempted to reset non-existent board: {board_id}")
        raise HTTPException(status_code=404, detail="Board not found")
    
    games[board_id] = initialize_game()
    logger.info(f"Board {board_id} has been reset")
    return {
        "board_id": board_id,
        "board": games[board_id]["board"],
        "message": "Board reset successfully"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)