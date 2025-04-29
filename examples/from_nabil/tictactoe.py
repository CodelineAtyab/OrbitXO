import random

# Display the board
def print_board(b):
    print()
    print(f" {b[0]} | {b[1]} | {b[2]}")
    print("---+---+---")
    print(f" {b[3]} | {b[4]} | {b[5]}")
    print("---+---+---")
    print(f" {b[6]} | {b[7]} | {b[8]}")
    print()

# Check for a win using if statements
def check_winner(b, s):
    if b[0] == s and b[1] == s and b[2] == s or \
       b[3] == s and b[4] == s and b[5] == s or \
       b[6] == s and b[7] == s and b[8] == s or \
       b[0] == s and b[3] == s and b[6] == s or \
       b[1] == s and b[4] == s and b[7] == s or \
       b[2] == s and b[5] == s and b[8] == s or \
       b[2] == s and b[4] == s and b[6] == s or \
       b[0] == s and b[4] == s and b[8] == s:
       return True
    return False 

# Get player move
def player_move(board):
    while True:
        move = input("Your move (1-9): ")
        if move.isdigit() and 1 <= int(move) <= 9:
            idx = int(move) - 1
            if board[idx] not in ['X','O']:
                return idx
        print("Invalid move, try again.")

# Get bot move
def bot_move(board):
    empty = []
    for i in range(9):
      if board[i]!="X" and board[i]!="O":
          empty.append(i)  
    return random.choice(empty)

# --- Game Execution Starts Here ---
print("Welcome to Tic Tac Toe!")
player = ''
while player not in ['X', 'O']:
    player = input("Choose your symbol (X or O): ").upper()

bot = 'O' if player == 'X' else 'X'
print(f"You are {player}, bot is {bot}. Let's play!")

board = [str(i+1) for i in range(9)]
print_board(board)

turn = 'player' if player == 'X' else 'bot'

for i in range(9):
    if turn == 'player':
        idx = player_move(board)
        board[idx] = player
        print_board(board)
        if check_winner(board, player):
            print("You win!")
            break
        turn = 'bot'
    else:
        print("Bot's move:")
        idx = bot_move(board)
        board[idx] = bot
        print_board(board)
        if check_winner(board, bot):
            print("Bot wins!")
            break
        turn = 'player'
else:
    print("It's a draw!")


