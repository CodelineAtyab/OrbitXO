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

def try_to_make_a_move(board, input_seq, input_seq_index, symbol, is_player_move):
  is_move_successfully_made = False
  while not is_move_successfully_made:
    is_move_successfully_made = make_move(board=board, 
                                          sel_row=int(input_seq[input_seq_index][0]), 
                                          sel_col=int(input_seq[input_seq_index][1]), 
                                          symbol=symbol)
    
    if is_move_successfully_made:
      input_seq_index = input_seq_index + 1
      return (not is_player_move, input_seq_index)
    
    # Failure Case
    input_seq_index = input_seq_index + 1