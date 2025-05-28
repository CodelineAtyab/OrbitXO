board = [
    ["-", "-", "-"],
    ["-", "-", "-"],
    ["-", "-", "-"]
    ]

def play_a_turn(pos1, pos2, symbol):
    board[pos1][pos2] = symbol
    print(str(board[0]) + "\n" + str(board[1]) + "\n" + str(board[2]) + "\n")

player_pos = ["11", "00", "21", "20", "12"]
bot_pos = ["10", "22", "01", "02"]
player_symbol = "X"
bot_symbol = "O"

for index in range(len(player_pos)):
    try:
        play_a_turn(int(player_pos[index][0]), int(player_pos[index][1]), player_symbol)

        play_a_turn(int(bot_pos[index][0]), int(bot_pos[index][1]), bot_symbol)
    except IndexError:
        pass