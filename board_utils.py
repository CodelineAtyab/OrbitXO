import time


def make_move(board, sel_row, sel_col, symbol):
  move_successful = False
  if board[sel_row][sel_col] == "-":
    if (sel_row >= 0 and sel_row <= 2) and (sel_col >= 0 and sel_col <= 2):
      # User 1 Makes a move
      board[sel_row][sel_col] = symbol
      move_successful = True
      print(f"{symbol} Move: {sel_row} - {sel_col}")

      # Print the entire board
      for row in board:
        print(row)
  else:
    print(f"Unable to make a move at {sel_row}-{sel_col} with {symbol}")
    
  time.sleep(1)
  return move_successful


def is_board_filled(board, empty_box_symbol):
  return empty_box_symbol not in str(board)