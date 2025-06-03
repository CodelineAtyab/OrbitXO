import time


EMPTY_SYMBOL = "-"


def make_move(board, sel_row, sel_col, symbol):
  move_successful = False
  if board[sel_row][sel_col] == EMPTY_SYMBOL:
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
    
  # time.sleep(1)
  return move_successful


def is_board_filled(board):
  return EMPTY_SYMBOL not in str(board)


def is_trio_a_match(board, pos1, pos2, pos3, symbol):
  return board[pos1[0]][pos1[1]] == symbol and \
         board[pos2[0]][pos2[1]] == symbol and \
         board[pos3[0]][pos3[1]] == symbol


def is_there_a_winner(board, symbol):
  is_a_winner = False
  # Check All Rows For the Win 
  for row in range(3):
    is_a_winner = is_a_winner or is_trio_a_match(board=board, pos1=(row, 0), pos2=(row, 1), pos3=(row, 2), symbol=symbol)
  
  # Check All Col For the Win
  for col in range(3):
    is_a_winner = is_a_winner or is_trio_a_match(board=board, pos1=(0, col), pos2=(1, col), pos3=(2, col), symbol=symbol)
  
  # # Check Diagonals
  is_a_winner = is_a_winner or is_trio_a_match(board=board, pos1=(0, 0), pos2=(1, 1), pos3=(2, 2), symbol=symbol)
  is_a_winner = is_a_winner or is_trio_a_match(board=board, pos1=(0, 2), pos2=(1, 1), pos3=(2, 0), symbol=symbol)

  return is_a_winner