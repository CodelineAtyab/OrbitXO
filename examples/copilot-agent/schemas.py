"""
Pydantic schemas for request and response validation.

This module defines all the data models used for API request/response validation
and serialization using Pydantic.
"""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PlayerBase(BaseModel):
    """Base schema for player data."""
    name: str = Field(..., description="Player's display name", min_length=1, max_length=100)


class PlayerCreate(PlayerBase):
    """Schema for creating a new player."""
    pass


class Player(PlayerBase):
    """Schema for player response data."""
    id: int = Field(..., description="Unique player identifier")
    created_at: datetime = Field(..., description="When the player was created")
    
    class Config:
        from_attributes = True


class GameCreate(BaseModel):
    """Schema for creating a new game."""
    creator_name: str = Field(..., description="Name of the player creating the game", min_length=1, max_length=100)


class JoinGameRequest(BaseModel):
    """Schema for joining an existing game."""
    player_name: str = Field(..., description="Name of the player joining the game", min_length=1, max_length=100)


class MakeMoveRequest(BaseModel):
    """Schema for making a move in the game."""
    player_id: int = Field(..., description="ID of the player making the move")
    row: int = Field(..., description="Row position (0-2)", ge=0, le=2)
    col: int = Field(..., description="Column position (0-2)", ge=0, le=2)


class GamePlayerInfo(BaseModel):
    """Schema for game player information."""
    player_id: int = Field(..., description="Player's unique identifier")
    player_name: str = Field(..., description="Player's display name")
    symbol: str = Field(..., description="Player's symbol (X or O)")
    joined_at: datetime = Field(..., description="When the player joined the game")
    
    class Config:
        from_attributes = True


class GameState(BaseModel):
    """Schema for complete game state information."""
    id: int = Field(..., description="Unique game identifier")
    board: List[List[str]] = Field(..., description="3x3 board state with symbols")
    status: str = Field(..., description="Current game status (waiting, playing, completed, draw)")
    players: List[GamePlayerInfo] = Field(..., description="List of players in the game")
    winner_id: Optional[int] = Field(None, description="ID of the winning player (if game is completed)")
    winner_name: Optional[str] = Field(None, description="Name of the winning player (if game is completed)")
    current_turn_symbol: Optional[str] = Field(None, description="Symbol of the player whose turn it is (X or O)")
    created_at: datetime = Field(..., description="When the game was created")
    completed_at: Optional[datetime] = Field(None, description="When the game was completed")
    
    class Config:
        from_attributes = True


class ScoreInfo(BaseModel):
    """Schema for individual score information."""
    player_id: int = Field(..., description="Player's unique identifier")
    player_name: str = Field(..., description="Player's display name")
    result: str = Field(..., description="Player's result (win, loss, draw)")
    created_at: datetime = Field(..., description="When the score was recorded")
    
    class Config:
        from_attributes = True


class GameScore(BaseModel):
    """Schema for complete game score information."""
    game_id: int = Field(..., description="Unique game identifier")
    status: str = Field(..., description="Final game status")
    winner_name: Optional[str] = Field(None, description="Name of the winning player")
    scores: List[ScoreInfo] = Field(..., description="List of individual player scores")
    completed_at: Optional[datetime] = Field(None, description="When the game was completed")
    
    class Config:
        from_attributes = True


class APIResponse(BaseModel):
    """Generic API response schema."""
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Human-readable message about the operation")
    data: Optional[dict] = Field(None, description="Response data (varies by endpoint)")


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    success: bool = Field(False, description="Always false for error responses")
    message: str = Field(..., description="Error message describing what went wrong")
    error_code: Optional[str] = Field(None, description="Machine-readable error code")
    details: Optional[dict] = Field(None, description="Additional error details")