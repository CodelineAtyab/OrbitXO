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
user_1_inp_sequence = ["00", "01", "02", "11", "22", "12", "00"]
bot_inp_sequence = ["12", "20", "10", "21", "20"]

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
      # Move was Made Successfully
      # Check who wins
      # Checking Rows for the Win
      print(board_utils.is_trio_a_match(board=board, pos1=(0, 0), pos2=(0, 1), pos3=(0, 2), symbol="X"))

      # Check All Rows For the Win 
      for row in range(3):
        is_a_winner = is_a_winner or board_utils.is_trio_a_match(board=board, pos1=(row, 0), pos2=(row, 1), pos3=(row, 2), symbol="X")
      
      # Check All Col For the Win
      for col in range(3):
        is_a_winner = is_a_winner or board_utils.is_trio_a_match(board=board, pos1=(0, col), pos2=(1, col), pos3=(2, col), symbol="X")
      
      # # Check Diagonals
      is_a_winner = is_a_winner or board_utils.is_trio_a_match(board=board, pos1=(0, 0), pos2=(1, 1), pos3=(2, 2), symbol="X")
      is_a_winner = is_a_winner or board_utils.is_trio_a_match(board=board, pos1=(0, 2), pos2=(1, 1), pos3=(2, 0), symbol="X")

  
    if not is_players_move:
      """
      Step 2 - Bot Makes a Move
      """
      is_players_move, bot_move_index = board_utils.try_to_make_a_move(board=board,
                                                                       input_seq=bot_inp_sequence,
                                                                       input_seq_index=bot_move_index, 
                                                                       symbol=bot_symbol,
                                                                       is_player_move=is_players_move)
      
      # Move was Made Successfully
      # Check who wins
    
    # print(board_utils.is_board_filled(board, EMPTY_SYMBOL))

  except IndexError:
    print("Board is already filled. Thanks!")
