def display_board(board):
    print()
    print(" " + board[0] + " | " + board[1] + " | " + board[2])
    print("---|---|---")
    print(" " + board[3] + " | " + board[4] + " | " + board[5])
    print("---|---|---")
    print(" " + board[6] + " | " + board[7] + " | " + board[8])
    print()

# Function to check if someone won
def check_winner(board, symbol):
    if (board[0] == symbol and board[1] == symbol and board[2] == symbol) or \
       (board[3] == symbol and board[4] == symbol and board[5] == symbol) or \
       (board[6] == symbol and board[7] == symbol and board[8] == symbol) or \
       (board[0] == symbol and board[3] == symbol and board[6] == symbol) or \
       (board[1] == symbol and board[4] == symbol and board[7] == symbol) or \
       (board[2] == symbol and board[5] == symbol and board[8] == symbol) or \
       (board[0] == symbol and board[4] == symbol and board[8] == symbol) or \
       (board[2] == symbol and board[4] == symbol and board[6] == symbol):
        return True
    else:
        return False

# Function to check for a draw
def check_draw(board):
    i = 0
    while i < 9:
        if board[i] != "X" and board[i] != "O":
            return False
        i = i + 1
    return True

# Function for the bot's move (first empty spot)
def bot_move(board, bot_symbol):
    i = 0
    while i < 9:
        if board[i] != "X" and board[i] != "O":
            board[i] = bot_symbol
            break
        i = i + 1
print("Welcome to Tic Tac Toe!")

# Player chooses symbol
player_symbol = ""
while player_symbol != "X" and player_symbol != "O":
    player_symbol = input("Choose your symbol (X or O): ").upper()

if player_symbol == "X":
    bot_symbol = "O"
else:
    bot_symbol = "X"

print("You are", player_symbol, "Bot is", bot_symbol)
print("Board positions:")
print(" 1 | 2 | 3 ")
print("---|---|---")
print(" 4 | 5 | 6 ")
print("---|---|---")
print(" 7 | 8 | 9 ")

# Initialize the board
board = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]

# Main Game Loop
while True:
    display_board(board)
    
    # Player's move
    move = input("Your move (1-9): ")
    if move not in board:
        print("Invalid move. Try again.")
        continue
    else:
        i = 0
        while i < 9:
            if board[i] == move:
                board[i] = player_symbol
                break
            i = i + 1

    if check_winner(board, player_symbol):
        display_board(board)
        print("You win!")
        break

    if check_draw(board):
        display_board(board)
        print("It's a draw!")
        break

    # Bot's move
    print("Bot's move:")
    bot_move(board, bot_symbol)

    if check_winner(board, bot_symbol):
        display_board(board)
        print("Bot wins!")
        break

    if check_draw(board):
        display_board(board)
        print("It's a draw!")
        break
