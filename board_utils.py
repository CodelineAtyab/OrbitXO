import time

def make_move(board, sel_row, sel_col, symbol):
  # Validation
  if (sel_row >= 0 and sel_row <= 2) and (sel_col >= 0 and sel_col <= 2):
    # User 1 Makes a move
    board[sel_row][sel_col] = symbol
    print(f"User 1 Move: {sel_row} - {sel_col}")

    # Print the entire board
    for row in board:
      print(row)
    
    # time.sleep(1)