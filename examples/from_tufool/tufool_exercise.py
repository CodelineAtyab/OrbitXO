import random

# Initialize board
board = [str(i) for i in range(1, 10)]

# Welcome message and symbol selection
print("Welcome to Tic Tac Toe!")
player_symbol = input("Choose your symbol (X or O): ").upper()

while player_symbol != 'X' and player_symbol != 'O':
    player_symbol = input("Invalid choice. Please choose X or O: ").upper()

bot_symbol = 'O' if player_symbol == 'X' else 'X'
print(f"You are {player_symbol}, the bot is {bot_symbol}. Let's start!")

# Print board
print()
print(f"{board[0]} | {board[1]} | {board[2]}")
print("--+---+--")
print(f"{board[3]} | {board[4]} | {board[5]}")
print("--+---+--")
print(f"{board[6]} | {board[7]} | {board[8]}")
print()

# Game loop
game_over = False

while not game_over:
    # --- Player Move ---
    valid_move = False
    while not valid_move:
        try:
            move = int(input("Your move (1-9): "))
            if move < 1 or move > 9:
                print("Please enter a number between 1 and 9.")
            elif board[move - 1] in ['X', 'O']:
                print("Spot already taken. Choose another one.")
            else:
                board[move - 1] = player_symbol
                valid_move = True
        except:
            print("Invalid input. Please enter a number.")

    # Print board
    print()
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()

    # Check for win
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == player_symbol:
            print("Congratulations! You win!")
            game_over = True
            break

    if game_over:
        break

    # Check for draw
    if all(spot in ['X', 'O'] for spot in board):
        print("It's a draw!")
        break

    # --- Bot Move ---
    available_moves = [i for i in range(9) if board[i] not in ['X', 'O']]
    bot_move = random.choice(available_moves)
    board[bot_move] = bot_symbol
    print(f"Bot chose position {bot_move + 1}")

    # Print board
    print()
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()

    # Check if bot wins
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] == bot_symbol:
            print("Bot wins! Better luck next time.")
            game_over = True
            break

    if game_over:
        break

    # Check for draw again
    if all(spot in ['X', 'O'] for spot in board):
        print("It's a draw!")
        break