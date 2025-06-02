import random

import board_utils
from utils import convert_two_digit_string_to_tuple


EMPTY_SYMBOL = "-"

board = [
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
]

ALL_POSITIONS = ("00", "01", "02", "10", "11", "12", "20", "21", "22")

user_1_symbol = "X"
bot_symbol = "O"

# Player Winning Input Sequence
# user_1_inp_sequence = ["00", "01", "02", "11", "22", "12", "00"]
# bot_inp_sequence = ["12", "20", "10", "21", "20"]

# Draw Input Sequence
# user_1_inp_sequence = ["00", "20", "22", "01", "12"]
# bot_inp_sequence = ["02", "10", "11", "22", "21"]

# user_move_index = 0
# bot_move_index = 0

is_players_move = True
is_a_winner = False

# Process
while not board_utils.is_board_filled(board, EMPTY_SYMBOL) and not is_a_winner:
  try:
    if is_players_move:
      """
      Step 1 - User Makes a Move
      """
      player_move_location = convert_two_digit_string_to_tuple(input("Enter Your Move: "))
      is_players_move, user_move_index = board_utils.try_to_make_a_move(board=board,
                                                                        move_location=player_move_location,
                                                                        symbol=user_1_symbol,
                                                                        is_player_move=is_players_move)

      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="X")

    if not is_players_move and not is_a_winner:
      """
      Step 2 - Bot Makes a Move
      """
      bot_move_location = convert_two_digit_string_to_tuple(random.choice(ALL_POSITIONS))
      is_players_move, bot_move_index = board_utils.try_to_make_a_move(board=board,
                                                                       move_location=bot_move_location,
                                                                       symbol=bot_symbol,
                                                                       is_player_move=is_players_move)
      
      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="O")

  except IndexError:
    print("Board is already filled. Thanks!")

# Handle the Winner Announcement
if is_a_winner:
  if is_players_move == False:
    print("Player Wins")
  else:
    print("Bot Wins")
else:
  print("Its a Draw!")