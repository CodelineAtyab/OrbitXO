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
user_1_inp_sequence = ["00", "02", "11", "12", "01", "20", "00"]
bot_inp_sequence = ["02", "22", "10", "21", "22"]

user_move_index = 0
bot_move_index = 0

is_players_move = True

# Process
while not board_utils.is_board_filled(board, EMPTY_SYMBOL):
  try:
    if is_players_move:
      """
      Step 1 - User Makes a Move
      """
      is_players_move, user_move_index = board_utils.try_to_make_a_move(board=board,
                                                                        input_seq=user_1_inp_sequence,
                                                                        input_seq_index=user_move_index,
                                                                        symbol=user_1_symbol,
                                                                        is_player_move=is_players_move)
    
    if not is_players_move:
      """
      Step 2 - Bot Makes a Move
      """
      is_players_move, bot_move_index = board_utils.try_to_make_a_move(board=board,
                                                                       input_seq=bot_inp_sequence,
                                                                       input_seq_index=bot_move_index, 
                                                                       symbol=bot_symbol,
                                                                       is_player_move=is_players_move)
    
    print(board_utils.is_board_filled(board, EMPTY_SYMBOL))

  except IndexError:
    print("Board is already filled. Thanks!")
