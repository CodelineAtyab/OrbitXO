"""
Database models for the tic-tac-toe API.

This module defines SQLAlchemy models for storing game data including
players, games, game-player relationships, and final scores.
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Database configuration
DATABASE_URL = "sqlite:///./tictactoe.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Player(Base):
    """
    Player model representing a game player.
    
    Attributes:
        id: Unique identifier for the player
        name: Player's display name
        created_at: Timestamp when player was created
    """
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game_players = relationship("GamePlayer", back_populates="player")


class Game(Base):
    """
    Game model representing a tic-tac-toe game instance.
    
    Attributes:
        id: Unique identifier for the game
        board_state: JSON string representing the 3x3 board state
        status: Current game status (waiting, playing, completed, draw)
        winner_id: ID of the winning player (null if no winner yet)
        created_at: Timestamp when game was created
        completed_at: Timestamp when game was completed
    """
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    board_state = Column(Text, default='[["","",""],["","",""],["","",""]]')  # JSON string
    status = Column(String(20), default="waiting")  # waiting, playing, completed, draw
    winner_id = Column(Integer, ForeignKey("players.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    winner = relationship("Player", foreign_keys=[winner_id])
    game_players = relationship("GamePlayer", back_populates="game")
    scores = relationship("Score", back_populates="game")


class GamePlayer(Base):
    """
    GamePlayer model representing the relationship between games and players.
    
    This model tracks which players are in which games and what symbol they use.
    
    Attributes:
        id: Unique identifier for the game-player relationship
        game_id: Foreign key to the game
        player_id: Foreign key to the player
        symbol: The symbol used by this player in this game (X or O)
        joined_at: Timestamp when player joined the game
    """
    __tablename__ = "game_players"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    symbol = Column(String(1), nullable=False)  # X or O
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("Game", back_populates="game_players")
    player = relationship("Player", back_populates="game_players")


class Score(Base):
    """
    Score model representing the final result of a completed game.
    
    This model stores the outcome for each player in a completed game.
    
    Attributes:
        id: Unique identifier for the score record
        game_id: Foreign key to the game
        player_id: Foreign key to the player
        player_name: Player's name (denormalized for easier access)
        result: Result for this player (win, loss, draw)
        created_at: Timestamp when score was recorded
    """
    __tablename__ = "scores"
    
    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    player_name = Column(String(100), nullable=False)
    result = Column(String(10), nullable=False)  # win, loss, draw
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    game = relationship("Game", back_populates="scores")
    player = relationship("Player")


def create_tables():
    """Create all database tables."""
    Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency function to get database session.
    
    Yields:
        Database session that automatically closes after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()