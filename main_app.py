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
    # Access global variables to track game state
    global is_players_move  # Controls whose turn it is (True = player, False = bot)
    global is_a_winner      # Tracks if someone has won the game (True/False)

    if is_players_move:
      """
      Step 1 - User Makes a Move
      
      In this section, we handle the player's move. The player provides a move 
      in the format "row column" (e.g., "00" for top-left, "12" for middle-right).
      """
      # Call player_utils to attempt to make the player's move
      # This returns False if move was successful (to switch turns)
      # Returns None if move was invalid (e.g., cell already occupied)
      # Example: If player sends "11", we try to place X in the center cell
      is_players_move = player_utils.try_to_make_a_move(board=board,
                                                        symbol=user_1_symbol,
                                                        incoming_move=move,
                                                        is_player_move=is_players_move)
      
      # If the move was invalid (is_players_move is None), inform the user
      # Example: If player tries to place X on an already occupied cell
      if is_players_move is None:
        return {"msg": "Move is invalid", "board": board}

      # After player's move, check if they've won
      # Checks for 3 X's in a row, column, or diagonal
      is_a_winner = board_utils.is_there_a_winner(board=board, symbol="X")

    # Bot's turn - only proceeds if:
    # 1. It's not the player's turn (player move was successful)
    # 2. Nobody has won yet
    # 3. The board isn't completely filled
    if not is_players_move and not is_a_winner and not board_utils.is_board_filled(board):
      """
      Step 2 - Bot Makes a Move
      
      After the player makes a valid move, the bot automatically makes its move.
      The bot_utils handles the AI logic for selecting the best move.
      """
      # The bot makes its move automatically
      # This returns True to give the turn back to the player
      # Example: Bot might place O at "02" (top-right corner)
      is_players_move = bot_utils.try_to_make_a_move(board=board,
                                                     symbol=bot_symbol,
                                                     is_player_move=is_players_move)
      
      # After bot's move, check if it has won
      # Checks for 3 O's in a row, column, or diagonal
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

if __name__ == "__main__":
  print(perform_move("00"))
  print(perform_move("02"))
  print(perform_move("22"))
  print(perform_move("11"))
