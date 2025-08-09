# Tic-Tac-Toe FastAPI Application

A comprehensive, well-documented FastAPI-based tic-tac-toe API that allows two players to create and play games with persistent data storage in SQLite. This implementation meets all requirements for a professional tic-tac-toe game API with detailed documentation.

## Features

- ✅ **Game Creation**: Create new tic-tac-toe games with unique IDs
- ✅ **Two-Player Support**: Exactly two players can join each game (X and O symbols)
- ✅ **Move Validation**: Comprehensive move validation and turn management
- ✅ **Win Detection**: Automatic detection of wins and draws
- ✅ **Readonly Boards**: Board becomes readonly after game completion
- ✅ **Player Management**: Track players with unique IDs and names
- ✅ **Score Tracking**: Persistent score recording with game results
- ✅ **SQLite Storage**: All data persisted to SQLite database
- ✅ **Comprehensive Documentation**: Detailed comments on every public method
- ✅ **API Documentation**: Auto-generated OpenAPI/Swagger documentation

## Quick Start

### Option 1: Automatic Setup
```bash
./start_server.sh
```

### Option 2: Manual Setup
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

### Core Game Operations
- **`POST /games`** - Create a new game with a player
- **`POST /games/{game_id}/join`** - Join an existing game (max 2 players)
- **`GET /games/{game_id}`** - Get complete game state
- **`POST /games/{game_id}/move`** - Make a move on the board

### Information Retrieval
- **`GET /players/{player_id}`** - Get player information
- **`GET /games/{game_id}/score`** - Get final game score and results
- **`GET /`** - API information and health check

## Usage Example

1. **Create a game:**
```bash
curl -X POST "http://localhost:8000/games" \
     -H "Content-Type: application/json" \
     -d '{"creator_name": "Alice"}'
```

2. **Join the game:**
```bash
curl -X POST "http://localhost:8000/games/1/join" \
     -H "Content-Type: application/json" \
     -d '{"player_name": "Bob"}'
```

3. **Make a move:**
```bash
curl -X POST "http://localhost:8000/games/1/move" \
     -H "Content-Type: application/json" \
     -d '{"player_id": 1, "row": 0, "col": 0}'
```

4. **Check game state:**
```bash
curl -X GET "http://localhost:8000/games/1"
```

5. **Get final score (after game completion):**
```bash
curl -X GET "http://localhost:8000/games/1/score"
```

## Testing

Run the demo script to see a complete game example:
```bash
# Start the server first
uvicorn main:app --reload

# In another terminal, run the demo
python test_demo.py
```

## Database Schema

The application uses SQLite with the following tables:

- **`players`** - Store player information (id, name, created_at)
- **`games`** - Store game state (id, board_state, status, winner_id, timestamps)
- **`game_players`** - Link players to games with their symbols
- **`scores`** - Store final game results for each player

## Architecture

- **`main.py`** - FastAPI application with all endpoints
- **`models.py`** - SQLAlchemy database models
- **`schemas.py`** - Pydantic schemas for request/response validation
- **`game_logic.py`** - Pure game logic functions (board validation, win detection)
- **`requirements.txt`** - Python dependencies
- **`test_demo.py`** - Demo script showing API usage

## Game Rules

1. Two players take turns placing X and O on a 3x3 grid
2. Player with X always goes first
3. First player to get three in a row (horizontal, vertical, or diagonal) wins
4. If all positions are filled without a winner, the game is a draw
5. Once a game is completed, the board becomes readonly
6. Scores are automatically recorded for both players