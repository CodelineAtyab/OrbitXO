import board_utils

board = [
  ["-", "-", "-"],  # 00 01 02
  ["-", "-", "-"],  # 10 11 12
  ["-", "-", "-"]   # 20 21 22
]

all_positions = ["00", "01", "02", "10", "11", "12", "20", "21", "22"]

user_1_symbol = "X"
bot_symbol = "O"
user_1_inp_sequence = ["00", "11", "12", "01", "20"]
bot_inp_sequence = ["02", "22", "10", "21"]

# Process
for index in range(0, len(user_1_inp_sequence)):
  """
  Step 1 - User Makes a Move
  """
  try:
    board_utils.make_move(board=board, 
                          sel_row=int(user_1_inp_sequence[index][0]), 
                          sel_col=int(user_1_inp_sequence[index][1]), 
                          symbol=user_1_symbol)

    """
    Step 2 - Bot Makes a Move
    """
    board_utils.make_move(board=board, 
                          sel_row=int(bot_inp_sequence[index][0]), 
                          sel_col=int(bot_inp_sequence[index][1]), 
                          symbol=bot_symbol)
  except IndexError:
    print("Board is already filled. Thanks!")