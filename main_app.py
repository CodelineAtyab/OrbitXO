import board_utils
import bot_utils
import player_utils
from board_utils import EMPTY_SYMBOL


board = [
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
  [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
]

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
while not board_utils.is_board_filled(board) and not is_a_winner:
  try:
    if is_players_move:
      """
      Step 1 - User Makes a Move
      """
      is_players_move = player_utils.try_to_make_a_move(board=board,
                                                        symbol=user_1_symbol,
                                                        is_player_move=is_players_move)

      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="X")

    if not is_players_move and not is_a_winner and not board_utils.is_board_filled(board):
      """
      Step 2 - Bot Makes a Move
      """
      is_players_move = bot_utils.try_to_make_a_move(board=board,
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