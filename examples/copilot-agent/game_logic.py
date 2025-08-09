"""
Game logic utilities for tic-tac-toe.

This module contains all the core game logic including board validation,
win condition checking, and move processing.
"""

import json
from typing import List, Optional, Tuple


def create_empty_board() -> List[List[str]]:
    """
    Create an empty 3x3 tic-tac-toe board.
    
    Returns:
        A 3x3 list of empty strings representing an empty board
    """
    return [["", "", ""], ["", "", ""], ["", "", ""]]


def board_to_string(board: List[List[str]]) -> str:
    """
    Convert a board list to a JSON string for database storage.
    
    Args:
        board: 3x3 list representing the game board
        
    Returns:
        JSON string representation of the board
    """
    return json.dumps(board)


def board_from_string(board_str: str) -> List[List[str]]:
    """
    Convert a JSON string back to a board list.
    
    Args:
        board_str: JSON string representation of the board
        
    Returns:
        3x3 list representing the game board
    """
    return json.loads(board_str)


def is_valid_move(board: List[List[str]], row: int, col: int) -> bool:
    """
    Check if a move is valid (position is empty and within bounds).
    
    Args:
        board: Current 3x3 board state
        row: Row position (0-2)
        col: Column position (0-2)
        
    Returns:
        True if the move is valid, False otherwise
    """
    # Check bounds
    if row < 0 or row > 2 or col < 0 or col > 2:
        return False
    
    # Check if position is empty
    return board[row][col] == ""


def make_move(board: List[List[str]], row: int, col: int, symbol: str) -> List[List[str]]:
    """
    Make a move on the board by placing a symbol at the specified position.
    
    Args:
        board: Current 3x3 board state
        row: Row position (0-2)
        col: Column position (0-2)
        symbol: Symbol to place (X or O)
        
    Returns:
        Updated board with the new move
        
    Raises:
        ValueError: If the move is invalid
    """
    if not is_valid_move(board, row, col):
        raise ValueError(f"Invalid move: position ({row}, {col}) is not available")
    
    # Create a copy of the board to avoid modifying the original
    new_board = [row[:] for row in board]
    new_board[row][col] = symbol
    return new_board


def check_winner(board: List[List[str]]) -> Optional[str]:
    """
    Check if there's a winner on the current board.
    
    Args:
        board: Current 3x3 board state
        
    Returns:
        The winning symbol (X or O) if there's a winner, None otherwise
    """
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    
    return None


def is_board_full(board: List[List[str]]) -> bool:
    """
    Check if the board is completely filled.
    
    Args:
        board: Current 3x3 board state
        
    Returns:
        True if all positions are filled, False otherwise
    """
    for row in board:
        for cell in row:
            if cell == "":
                return False
    return True


def is_game_over(board: List[List[str]]) -> Tuple[bool, Optional[str]]:
    """
    Check if the game is over and determine the result.
    
    Args:
        board: Current 3x3 board state
        
    Returns:
        Tuple of (is_over, result) where:
        - is_over: True if game is finished
        - result: 'win' if there's a winner, 'draw' if it's a draw, None if game continues
    """
    winner = check_winner(board)
    if winner:
        return True, 'win'
    
    if is_board_full(board):
        return True, 'draw'
    
    return False, None


def get_next_turn_symbol(board: List[List[str]], first_player_symbol: str = 'X') -> str:
    """
    Determine whose turn it is based on the current board state.
    
    Args:
        board: Current 3x3 board state
        first_player_symbol: Symbol of the player who goes first (default: X)
        
    Returns:
        Symbol of the player whose turn it is next
    """
    x_count = sum(row.count('X') for row in board)
    o_count = sum(row.count('O') for row in board)
    
    # X always goes first
    if x_count <= o_count:
        return 'X'
    else:
        return 'O'


def format_board_display(board: List[List[str]]) -> str:
    """
    Format the board for human-readable display.
    
    Args:
        board: Current 3x3 board state
        
    Returns:
        Formatted string representation of the board
    """
    display_board = []
    for i, row in enumerate(board):
        display_row = []
        for j, cell in enumerate(row):
            if cell == "":
                display_row.append(f"{i*3 + j + 1}")  # Show position numbers for empty cells
            else:
                display_row.append(cell)
        display_board.append(" | ".join(display_row))
    
    return "\n-----------\n".join(display_board)