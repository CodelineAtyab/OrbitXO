tictactoe_games = {}

EMPTY_SYMBOL = "-"

def empty_board():
    return [[EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
            [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
            [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL]]

def display_board(board_id):
    if board_id in tictactoe_games:
        return {"board":tictactoe_games[board_id]}
    else:
        return {"error":"Board not found"}
