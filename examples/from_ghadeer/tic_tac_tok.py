import random

# Function to print the board
def print_board(board):
    print()
    for i in range(3):
        print(f" {board[3*i]} | {board[3*i+1]} | {board[3*i+2]} ")
        if i < 2:
            print("-----------")
    print()

# Function to check if a player has won
def check_winner(board, symbol):
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for combo in win_combinations:
        if all(board[pos] == symbol for pos in combo):
            return True
    return False

# Function to check if the board is full (draw)
def is_draw(board):
    return all(space in ['X', 'O'] for space in board)

# Function to handle the player's move
def player_move(board, player_symbol):
    while True:
        try:
            move = int(input("Your move (choose a number 1-9): ")) - 1
            if move < 0 or move > 8:
                print("Invalid number. Please choose between 1 and 9.")
            elif board[move] in ['X', 'O']:
                print("That spot is already taken. Choose another one.")
            else:
                board[move] = player_symbol
                break
        except ValueError:
            print("Please enter a valid number.")

# Function for the bot's move
def bot_move(board, bot_symbol):
    available_moves = [i for i, spot in enumerate(board) if spot not in ['X', 'O']]
    move = random.choice(available_moves)
    board[move] = bot_symbol
    print(f"Bot chose position {move+1}.")

# Game setup and loop (formerly inside main)
board = [str(i+1) for i in range(9)]

print("Welcome to Tic Tac Toe!")
player_symbol = ''
while player_symbol not in ['X', 'O']:
    player_symbol = input("Choose your symbol (X or O): ").upper()

bot_symbol = 'O' if player_symbol == 'X' else 'X'
print(f"You are {player_symbol}, the bot is {bot_symbol}. Let's start!")

print_board(board)

# X always goes first
player_turn = True if player_symbol == 'X' else False

while True:
    if player_turn:
        player_move(board, player_symbol)
    else:
        bot_move(board, bot_symbol)
    
    print_board(board)

    if check_winner(board, player_symbol):
        print("Congratulations! You win!")
        break
    elif check_winner(board, bot_symbol):
        print("The bot wins! Better luck next time.")
        break
    elif is_draw(board):
        print("It's a draw!")
        break

    player_turn = not player_turn
