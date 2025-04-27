import random
print("Welcome to Tic Tac Toe!")
user_choice = input("Choose your symbol (X OR O): ") .upper()

# When the user choise X the bot will directly select the O
bot_choice = 'O' if user_choice == 'X' else 'X'


print(f"you are {user_choice}, the bot is {bot_choice}. Let's start!" )

# creating an empty board
board = [' ' for _ in range(9)]

#board display
def display_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("----+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("----+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]}")
    print()

    #function to define player move

def player_move(board, user_choice):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) -1
            if move < 0 or move > 8:
                print("Invalid position! choose a number between 1 and 9.")
            elif board[move] != ' ':
                print("Position already taken! choose another one.")
            else:
                board[move] = user_choice
                break

        except ValueError:
            print("Invalid input! please enter a number between 1 and 9.")

def bot_move(board, bot_choice):
    available_move = [i for i, spot in enumerate(board) if spot == ' ']
    move = random.choice(available_move)
    board[move] = bot_choice
    print(f"Bot placed {bot_choice} in position {move + 1}")
# using tuples for immutable and faster to read and also to protect logic
def check_winner(board, symbol):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for a, b, c in win_conditions:
        if board[a] == board[b] == board[c] == symbol:
            return True
    return False

def is_draw(board):
    return ' ' not in board

while True:
    display_board(board)
    player_move(board, user_choice)
    if check_winner(board, user_choice):
        display_board(board)
        print("Congratulations! You win!")
        break
    if is_draw(board):
        display_board(board)
        print("It's a draw!")
        break

    bot_move(board, bot_choice)
    if check_winner(board, bot_choice):
        display_board(board)
        print("Bot wins! Better luck next time.")
        break
    if is_draw(board):
        display_board(board)
        print("It's a draw!")
        break
