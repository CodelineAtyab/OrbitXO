tictactoe_games = {}

EMPTY_SYMBOL = "-"

def empty_board():
    return [[EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
            [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL],
            [EMPTY_SYMBOL, EMPTY_SYMBOL, EMPTY_SYMBOL]]

def display_boards():
    return {"boards": list(tictactoe_games.keys())}

def display_board(board_id):
    if board_id in tictactoe_games:
        return {"board":tictactoe_games[board_id]}
    else:
        return {"error":"Board not found"}
    
def turn_tracker(board_id):
    if board_id not in tictactoe_games:
        return {"error": "Board not found"}
    if tictactoe_games[board_id]["player_turn"] == "1":
        symbol = tictactoe_games[board_id]["player_1_symbol"]
    else:
        symbol = tictactoe_games[board_id]["player_2_symbol"]
    return {"player_turn": tictactoe_games[board_id]["player_turn"], 
            "symbol": symbol}