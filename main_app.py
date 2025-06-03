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

is_players_move = True
is_a_winner = False


def perform_move(move: str):
  msg_to_return = {"msg": "Success", "board": board}

  try:
    global is_players_move
    global is_a_winner

    if is_players_move:
      """
      Step 1 - User Makes a Move
      """
      is_players_move = player_utils.try_to_make_a_move(board=board,
                                                        symbol=user_1_symbol,
                                                        incoming_move=move,
                                                        is_player_move=is_players_move)
      
      # Invalid Move - Tell the User by responding
      if is_players_move is None:
        return {"msg": "Move is invalid", "board": board}

      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="X")

    if not is_players_move and not is_a_winner and not board_utils.is_board_filled(board):
      """
      Step 2 - Bot Makes a Move
      """
      is_players_move = bot_utils.try_to_make_a_move(board=board,
                                                     symbol=bot_symbol,
                                                     is_player_move=is_players_move)
      
      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="O")

    # Handle the Winner Announcement
    if is_a_winner:
      if is_players_move == False:
        msg_to_return["msg"] = "Player Wins!"
        print("Player Wins")
      else:
        msg_to_return["msg"] = "Bot Wins!"
        print("Bot Wins")
    elif board_utils.is_board_filled(board):
      msg_to_return["msg"] = "Its a Draw!"
      print("Its a Draw!")

    return msg_to_return

  except IndexError:
    err_msg = "Board is already filled. Thanks!"
    msg_to_return["msg"] = err_msg

    print(err_msg)
    return msg_to_return

# Process
# while not board_utils.is_board_filled(board) and not is_a_winner:
#   perform_move()

print(perform_move("00"))
print(perform_move("02"))
print(perform_move("22"))
print(perform_move("11"))
