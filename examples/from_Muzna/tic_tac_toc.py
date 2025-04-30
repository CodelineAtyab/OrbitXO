import random

board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

player = input("Choose your symbol (X or O): ").upper()

while player not in ["X", "O"]:
    player = input("Invalid choice. Please choose X or O: ").upper()

bot = "O" if player == "X" else "X"

print(f"You are {player}, the bot is {bot}. Let's start!")

def display_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}")
    print()

def player_move():
    while True:
        move = input("Your move (choose 1-9): ")
        if move in board:
            board[int(move) - 1] = player
            break
        else:
            print("Invalid move. Try again.")

def bot_move():
    #list of free positions in the board
    all_F_P = [pos for pos in board if pos not in ["X", "O"]]
    #choose any num from the list allFP
    move = random.choice(all_F_P)
    print(f"Bot chooses {move}")
    board[int(move) - 1] = bot

def check_win(symbol):
    win_combos = [[0, 1, 2],[3, 4, 5],[6, 7, 8],[0, 3, 6],[1, 4, 7],[2, 5, 8],[0, 4, 8],[2, 4, 6]]
    for combo in win_combos:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == symbol:
            return True
    return False

def check_draw():
    return all(space in ["X", "O"] for space in board)


while True:
    display_board()
    player_move()
    if check_win(player):
        display_board()
        print("Congratulations! You win!")
        break
    if check_draw():
        display_board()
        print("It's a draw!")
        break

    display_board()
    bot_move()
    if check_win(bot):
        display_board()
        print("Bot wins! Better luck next time.")
        break
    if check_draw():
        display_board()
        print("It's a draw!")
        break

