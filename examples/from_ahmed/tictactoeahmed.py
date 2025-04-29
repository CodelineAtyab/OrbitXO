import random

board = [['1', '2', '3'],
            ['4', '5', '6'],
            ['7', '8', '9']]
player = 'X'
bot = 'O'
def display_board():
    print()
    for row in board:
        print("  " + " | ".join(row))
        print(" -----------")
    print()
def check_winner(symbol):
    for i in range(3):
        if board[i][0] == symbol and board[i][1] == symbol and board[i][2] == symbol:
            return True
        if board[0][i] == symbol and board[1][i] == symbol and board[2][i] == symbol:
            return True
    if board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol:
        return True
    if board[0][2] == symbol and board[1][1] == symbol and board[2][0] == symbol:
        return True
    return False
def check_draw():
    for i in range(3):
        for j in range(3):
            if board[i][j] != 'X' and board[i][j] != 'O':
                return False
    return True
display_board()
turn = 'player'
while True:
    if turn == 'player':
        move = input("Choose a number (1-9): ")
        found = False
        for i in range(3):
            for j in range(3):
                if board[i][j] == move:
                    board[i][j] = player
                    found = True
        if not found:
            print("Invalid move!")
            continue
        display_board()
        if check_winner(player):
            print("You win!")
            break
        elif check_draw():
            print("It's a draw!")
            break
        else:
            turn = 'bot'
    else:
        moves = []
        for i in range(3):
            for j in range(3):
                if board[i][j] != 'X' and board[i][j] != 'O':
                    moves.append((i, j))
        move = random.choice(moves)
        board[move[0]][move[1]] = bot
        print("Bot's move:")
        display_board()
        if check_winner(bot):
            print("Bot wins!")
            break
        elif check_draw():
            print("It's a draw!")
            break
        else:
            turn = 'player'
