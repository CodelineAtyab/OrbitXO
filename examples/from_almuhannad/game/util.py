import uuid
games = {}

empty_symbol = "_"

def board():
    board_id = str (uuid.uuid4())
    games[board_id] = [
          [empty_symbol, empty_symbol, empty_symbol], 
            [empty_symbol, empty_symbol, empty_symbol],
            [empty_symbol, empty_symbol, empty_symbol]
            ]
    return board_id

def get_board(board_id):
    if board_id in games:
        return games[board_id]
    return None