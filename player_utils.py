from board_utils import make_move
from utils import convert_two_digit_string_to_tuple


def try_to_make_a_move(board, symbol, is_player_move):
  is_move_successfully_made = False
  while not is_move_successfully_made:
    player_move_location = convert_two_digit_string_to_tuple(input("Enter Your Move: "))
    is_move_successfully_made = make_move(board=board, 
                                          sel_row=player_move_location[0], 
                                          sel_col=player_move_location[1], 
                                          symbol=symbol)
    
    if is_move_successfully_made:
      return (not is_player_move)
  