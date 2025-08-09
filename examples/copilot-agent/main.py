"""
FastAPI Tic-Tac-Toe API

A comprehensive tic-tac-toe API that allows two players to create and play games
with persistent data storage in SQLite. This API provides endpoints for game
creation, player management, move execution, and score tracking.

Author: Copilot Agent
"""

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from datetime import datetime

# Import our modules
from models import get_db, create_tables, Player, Game, GamePlayer, Score
from schemas import (
    GameCreate, JoinGameRequest, MakeMoveRequest, GameState, 
    Player as PlayerSchema, GameScore, APIResponse, ErrorResponse,
    GamePlayerInfo, ScoreInfo
)
import game_logic

# Create FastAPI application instance
app = FastAPI(
    title="Tic-Tac-Toe API",
    description="A comprehensive API for playing tic-tac-toe games with two players",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Create database tables on startup
create_tables()


@app.get("/", response_model=APIResponse)
async def root():
    """
    Root endpoint providing API information.
    
    Returns:
        Basic API information and available endpoints
    """
    return APIResponse(
        success=True,
        message="Welcome to the Tic-Tac-Toe API",
        data={
            "version": "1.0.0",
            "description": "A comprehensive API for playing tic-tac-toe games",
            "documentation": "/docs",
            "endpoints": [
                "POST /games - Create a new game",
                "POST /games/{game_id}/join - Join an existing game",
                "GET /games/{game_id} - Get game state",
                "POST /games/{game_id}/move - Make a move",
                "GET /players/{player_id} - Get player information",
                "GET /games/{game_id}/score - Get final game score"
            ]
        }
    )


@app.post("/games", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
async def create_game(game_data: GameCreate, db: Session = Depends(get_db)):
    """
    Create a new tic-tac-toe game.
    
    This endpoint creates a new game with an empty board and adds the creator
    as the first player with symbol 'X'. The game will be in 'waiting' status
    until a second player joins.
    
    Args:
        game_data: Game creation data including creator's name
        db: Database session dependency
        
    Returns:
        API response with created game information
        
    Raises:
        HTTPException: If game creation fails
    """
    try:
        # Create or get the player
        player = db.query(Player).filter(Player.name == game_data.creator_name).first()
        if not player:
            player = Player(name=game_data.creator_name)
            db.add(player)
            db.commit()
            db.refresh(player)
        
        # Create new game with empty board
        empty_board = game_logic.create_empty_board()
        game = Game(
            board_state=game_logic.board_to_string(empty_board),
            status="waiting"
        )
        db.add(game)
        db.commit()
        db.refresh(game)
        
        # Add creator as first player (X)
        game_player = GamePlayer(
            game_id=game.id,
            player_id=player.id,
            symbol="X"
        )
        db.add(game_player)
        db.commit()
        
        return APIResponse(
            success=True,
            message=f"Game created successfully. Game ID: {game.id}",
            data={
                "game_id": game.id,
                "creator_name": player.name,
                "creator_symbol": "X",
                "status": "waiting",
                "message": "Waiting for second player to join"
            }
        )
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create game: {str(e)}"
        )


@app.post("/games/{game_id}/join", response_model=APIResponse)
async def join_game(game_id: int, join_data: JoinGameRequest, db: Session = Depends(get_db)):
    """
    Join an existing game as the second player.
    
    This endpoint allows a second player to join a game that's in 'waiting' status.
    The joining player will be assigned symbol 'O' and the game status will change
    to 'playing'.
    
    Args:
        game_id: ID of the game to join
        join_data: Join request data including player name
        db: Database session dependency
        
    Returns:
        API response with join confirmation
        
    Raises:
        HTTPException: If game doesn't exist, is full, or join fails
    """
    try:
        # Get the game
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        # Check if game is in waiting status
        if game.status != "waiting":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game is not accepting new players"
            )
        
        # Check if game already has 2 players
        existing_players = db.query(GamePlayer).filter(GamePlayer.game_id == game_id).count()
        if existing_players >= 2:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game is already full (2 players maximum)"
            )
        
        # Create or get the player
        player = db.query(Player).filter(Player.name == join_data.player_name).first()
        if not player:
            player = Player(name=join_data.player_name)
            db.add(player)
            db.commit()
            db.refresh(player)
        
        # Check if player is already in this game
        existing_game_player = db.query(GamePlayer).filter(
            GamePlayer.game_id == game_id,
            GamePlayer.player_id == player.id
        ).first()
        if existing_game_player:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Player is already in this game"
            )
        
        # Add player as second player (O)
        game_player = GamePlayer(
            game_id=game.id,
            player_id=player.id,
            symbol="O"
        )
        db.add(game_player)
        
        # Update game status to playing
        game.status = "playing"
        db.commit()
        
        return APIResponse(
            success=True,
            message=f"Successfully joined game {game_id}",
            data={
                "game_id": game.id,
                "player_name": player.name,
                "player_symbol": "O",
                "status": "playing",
                "message": "Game is ready to start! Player X goes first."
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to join game: {str(e)}"
        )


@app.get("/games/{game_id}", response_model=GameState)
async def get_game_state(game_id: int, db: Session = Depends(get_db)):
    """
    Get the current state of a game.
    
    This endpoint returns comprehensive information about the game including
    the board state, players, current turn, and game status.
    
    Args:
        game_id: ID of the game to retrieve
        db: Database session dependency
        
    Returns:
        Complete game state information
        
    Raises:
        HTTPException: If game doesn't exist
    """
    try:
        # Get the game
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        # Get game players with their information
        game_players = db.query(GamePlayer, Player).join(Player).filter(
            GamePlayer.game_id == game_id
        ).all()
        
        # Convert players to response format
        players_info = []
        for game_player, player in game_players:
            players_info.append(GamePlayerInfo(
                player_id=player.id,
                player_name=player.name,
                symbol=game_player.symbol,
                joined_at=game_player.joined_at
            ))
        
        # Get board state
        board = game_logic.board_from_string(game.board_state)
        
        # Determine current turn
        current_turn_symbol = None
        if game.status == "playing":
            current_turn_symbol = game_logic.get_next_turn_symbol(board)
        
        # Get winner information
        winner_name = None
        if game.winner_id:
            winner = db.query(Player).filter(Player.id == game.winner_id).first()
            if winner:
                winner_name = winner.name
        
        return GameState(
            id=game.id,
            board=board,
            status=game.status,
            players=players_info,
            winner_id=game.winner_id,
            winner_name=winner_name,
            current_turn_symbol=current_turn_symbol,
            created_at=game.created_at,
            completed_at=game.completed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get game state: {str(e)}"
        )


@app.post("/games/{game_id}/move", response_model=APIResponse)
async def make_move(game_id: int, move_data: MakeMoveRequest, db: Session = Depends(get_db)):
    """
    Make a move in the game.
    
    This endpoint allows a player to make a move by placing their symbol
    on the board. It validates the move, updates the board, checks for
    win conditions, and manages game completion.
    
    Args:
        game_id: ID of the game to make a move in
        move_data: Move request data including player ID and position
        db: Database session dependency
        
    Returns:
        API response with move result and updated game state
        
    Raises:
        HTTPException: If move is invalid or game is not playable
    """
    try:
        # Get the game
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        # Check if game is playable
        if game.status != "playing":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Game is not playable. Current status: {game.status}"
            )
        
        # Get player and verify they're in this game
        game_player = db.query(GamePlayer).filter(
            GamePlayer.game_id == game_id,
            GamePlayer.player_id == move_data.player_id
        ).first()
        if not game_player:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Player is not part of this game"
            )
        
        # Get current board state
        board = game_logic.board_from_string(game.board_state)
        
        # Check if it's the player's turn
        current_turn_symbol = game_logic.get_next_turn_symbol(board)
        if game_player.symbol != current_turn_symbol:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"It's not your turn. Current turn: {current_turn_symbol}"
            )
        
        # Validate and make the move
        if not game_logic.is_valid_move(board, move_data.row, move_data.col):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid move: position ({move_data.row}, {move_data.col}) is not available"
            )
        
        # Make the move
        new_board = game_logic.make_move(board, move_data.row, move_data.col, game_player.symbol)
        
        # Check if game is over
        is_over, result = game_logic.is_game_over(new_board)
        
        # Update game state
        game.board_state = game_logic.board_to_string(new_board)
        
        response_data = {
            "game_id": game.id,
            "player_symbol": game_player.symbol,
            "position": {"row": move_data.row, "col": move_data.col},
            "board": new_board
        }
        
        if is_over:
            game.completed_at = datetime.utcnow()
            
            if result == "win":
                # Player who just moved won
                game.status = "completed"
                game.winner_id = move_data.player_id
                
                # Create score records
                await _create_score_records(db, game_id, move_data.player_id)
                
                response_data["game_over"] = True
                response_data["result"] = "win"
                response_data["winner"] = game_player.symbol
                message = f"Game over! Player {game_player.symbol} wins!"
                
            else:  # Draw
                game.status = "draw"
                
                # Create score records for draw
                await _create_score_records(db, game_id, None)
                
                response_data["game_over"] = True
                response_data["result"] = "draw"
                message = "Game over! It's a draw!"
        else:
            # Game continues
            next_turn = game_logic.get_next_turn_symbol(new_board)
            response_data["next_turn"] = next_turn
            message = f"Move successful! Next turn: {next_turn}"
        
        db.commit()
        
        return APIResponse(
            success=True,
            message=message,
            data=response_data
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to make move: {str(e)}"
        )


async def _create_score_records(db: Session, game_id: int, winner_id: int = None):
    """
    Create score records for a completed game.
    
    This helper function creates score records for all players in a completed game,
    marking each player's result as win, loss, or draw.
    
    Args:
        db: Database session
        game_id: ID of the completed game
        winner_id: ID of the winning player (None for draw)
    """
    # Get all players in the game
    game_players = db.query(GamePlayer, Player).join(Player).filter(
        GamePlayer.game_id == game_id
    ).all()
    
    for game_player, player in game_players:
        if winner_id is None:
            # Draw game
            result = "draw"
        elif player.id == winner_id:
            # Winner
            result = "win"
        else:
            # Loser
            result = "loss"
        
        score = Score(
            game_id=game_id,
            player_id=player.id,
            player_name=player.name,
            result=result
        )
        db.add(score)


@app.get("/players/{player_id}", response_model=PlayerSchema)
async def get_player(player_id: int, db: Session = Depends(get_db)):
    """
    Get information about a specific player.
    
    This endpoint returns basic information about a player including
    their ID, name, and creation date.
    
    Args:
        player_id: ID of the player to retrieve
        db: Database session dependency
        
    Returns:
        Player information
        
    Raises:
        HTTPException: If player doesn't exist
    """
    try:
        player = db.query(Player).filter(Player.id == player_id).first()
        if not player:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Player not found"
            )
        
        return PlayerSchema(
            id=player.id,
            name=player.name,
            created_at=player.created_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get player: {str(e)}"
        )


@app.get("/games/{game_id}/score", response_model=GameScore)
async def get_game_score(game_id: int, db: Session = Depends(get_db)):
    """
    Get the final score and results for a completed game.
    
    This endpoint returns comprehensive score information for a completed game,
    including individual player results and the overall game outcome.
    
    Args:
        game_id: ID of the game to get scores for
        db: Database session dependency
        
    Returns:
        Complete game score information
        
    Raises:
        HTTPException: If game doesn't exist or is not completed
    """
    try:
        # Get the game
        game = db.query(Game).filter(Game.id == game_id).first()
        if not game:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Game not found"
            )
        
        # Check if game is completed
        if game.status not in ["completed", "draw"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Game is not completed yet"
            )
        
        # Get scores
        scores = db.query(Score).filter(Score.game_id == game_id).all()
        
        # Convert to response format
        score_info = []
        for score in scores:
            score_info.append(ScoreInfo(
                player_id=score.player_id,
                player_name=score.player_name,
                result=score.result,
                created_at=score.created_at
            ))
        
        # Get winner name
        winner_name = None
        if game.winner_id:
            winner = db.query(Player).filter(Player.id == game.winner_id).first()
            if winner:
                winner_name = winner.name
        
        return GameScore(
            game_id=game.id,
            status=game.status,
            winner_name=winner_name,
            scores=score_info,
            completed_at=game.completed_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get game score: {str(e)}"
        )


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Handle 404 errors with custom response."""
    return ErrorResponse(
        success=False,
        message="Resource not found",
        error_code="NOT_FOUND"
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Handle 500 errors with custom response."""
    return ErrorResponse(
        success=False,
        message="Internal server error",
        error_code="INTERNAL_ERROR"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)