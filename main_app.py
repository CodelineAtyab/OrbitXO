import board_utils


EMPTY_SYMBOL = "-"

board = [
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
]

all_positions = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]

user_1_symbol = "X"
bot_symbol = "O"
user_1_inp_sequence = ["00", "11", "12", "01", "20", "00"]
bot_inp_sequence = ["02", "22", "10", "21", "22"]

user_move_index = 0
bot_move_index = 0

is_players_move = True

# Process
for index in range(0, len(user_1_inp_sequence)):
  """
  Step 1 - User Makes a Move
  """
  try:
    if is_players_move:
      board_utils.make_move(board=board, 
                            sel_row=int(user_1_inp_sequence[index][0]), 
                            sel_col=int(user_1_inp_sequence[index][1]), 
                            symbol=user_1_symbol)
      is_players_move = False
    
    if not is_players_move:
      """
      Step 2 - Bot Makes a Move
      """
      is_move_successfully_made = False
      while not is_move_successfully_made:
        is_move_successfully_made = board_utils.make_move(board=board, 
                                                          sel_row=int(bot_inp_sequence[index][0]), 
                                                          sel_col=int(bot_inp_sequence[index][1]), 
                                                          symbol=bot_symbol)
        if not is_move_successfully_made:
          pass
        else:
          is_players_move = True
    
    print(board_utils.is_board_filled(board, EMPTY_SYMBOL))

  except IndexError:
    print("Board is already filled. Thanks!")
