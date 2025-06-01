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

user_1_inp_sequence = ["12", "20", "10", "21", "20"]
bot_inp_sequence = ["00", "01", "02", "11", "22", "12", "00"]

user_move_index = 0
bot_move_index = 0

is_players_move = True
is_a_winner = False

# Process
while not board_utils.is_board_filled(board, EMPTY_SYMBOL) and not is_a_winner:
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

      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="X")

    if not is_players_move and not is_a_winner:
      """
      Step 2 - Bot Makes a Move
      """
      is_players_move, bot_move_index = board_utils.try_to_make_a_move(board=board,
                                                                       input_seq=bot_inp_sequence,
                                                                       input_seq_index=bot_move_index, 
                                                                       symbol=bot_symbol,
                                                                       is_player_move=is_players_move)
      
      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="O")

  except IndexError:
    print("Board is already filled. Thanks!")
