# Tic-Tac-Toe FastAPI Application

A well-documented FastAPI-based tic-tac-toe API that allows two players to create and play games with persistent data storage in SQLite.

## Features

- Create new tic-tac-toe games
- Two players can join a game (X and O symbols)
- Make moves on the game board
- Automatic win detection and game completion
- Readonly board after game completion
- Player and score tracking
- SQLite database for data persistence

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn main:app --reload
```

3. Access the API documentation at `http://localhost:8000/docs`

## API Endpoints

- `POST /games` - Create a new game
- `POST /games/{game_id}/join` - Join an existing game
- `GET /games/{game_id}` - Get game state
- `POST /games/{game_id}/move` - Make a move
- `GET /players/{player_id}` - Get player information
- `GET /games/{game_id}/score` - Get final game score