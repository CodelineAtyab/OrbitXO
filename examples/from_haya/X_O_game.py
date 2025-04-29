import random

board = [['1', '2', '3'],
         ['4', '5', '6'],
         ['7', '8', '9']]

def display_board():
    print()
    for row in board:
        print("  " + " | ".join(row))
        if row != board[-1]:
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
            if board[i][j] not in ['X', 'O']:
                return False
    return True


while True:
    player = input("Choose your symbol (X or O): ").upper()
    if player in ['X', 'O']:
        break
    else:
        print("Invalid choice! Please choose X or O.")

bot = 'O' if player == 'X' else 'X'

display_board()

turn = 'player' if player == 'X' else 'bot'

while True:
    if turn == 'player':
        move = input("Choose a number (1-9): ")
        if not move.isdigit() or int(move) < 1 or int(move) > 9:
            print("Invalid input! Enter a number from 1 to 9.")
            continue

        found = False
        for i in range(3):
            for j in range(3):
                if board[i][j] == move:
                    board[i][j] = player
                    found = True
        if not found:
            print("Invalid move! Try again.")
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
                if board[i][j] not in ['X', 'O']:
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
