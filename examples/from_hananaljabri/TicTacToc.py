import random

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 5)
    print("\n")

def check_winner(board, symbol):
    # Check rows
    for row in board:
        count = 0
        for cell in row:
            if cell == symbol:
                count += 1
        if count == 3:
            return True

    # Check columns
    for col in range(3):
        count = 0
        for row in board:
            if row[col] == symbol:
                count += 1
        if count == 3:
            return True

    # Check diagonal from top-left to bottom-right
    count = 0
    for i in range(3):
        if board[i][i] == symbol:
            count += 1
    if count == 3:
        return True

    # Check diagonal from top-right to bottom-left
    count = 0
    for i in range(3):
        if board[i][2 - i] == symbol:
            count += 1
    if count == 3:
        return True

    return False

def is_draw(board):
    for row in board:
        for cell in row:
            if cell != "X" and cell != "O":
                return False
    return True

def get_available_moves(board):
    moves = []
    for i in range(3):
        for j in range(3):
            if board[i][j] != "X" and board[i][j] != "O":
                moves.append((i, j))
    return moves

def bot_move(board, bot_symbol):
    moves = get_available_moves(board)
    return random.choice(moves)

def play_game():
    board = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"]
    ]

    print("Welcome to Tic Tac Toe!")
    player_symbol = input("Choose your symbol (X or O): ").upper()

    while player_symbol != "X" and player_symbol != "O":
        player_symbol = input("Invalid choice. Please choose X or O: ").upper()

    if player_symbol == "X":
        bot_symbol = "O"
        turn = "Player"
    else:
        bot_symbol = "X"
        turn = "Bot"

    print_board(board)

    while True:
        if turn == "Player":
            move = input("Enter the number where you want to put your symbol: ")
 
            if not move.isdigit():
                print("Please enter a number from 1 to 9.")
                continue

            move = int(move)
            if move < 1 or move > 9:
                print("Invalid number. Please choose between 1 and 9.")
                continue

            row = (move - 1) // 3
            col = (move - 1) % 3

            if board[row][col] == "X" or board[row][col] == "O":
                print("This cell is already taken. Try again.")
                continue

            board[row][col] = player_symbol
            print_board(board)

            if check_winner(board, player_symbol):
                print("Congratulations! You win!")
                break

            if is_draw(board):
                print("It's a draw!")
                break

            turn = "Bot"

        else:
            print("Bot is making a move...")
            row, col = bot_move(board, bot_symbol)
            board[row][col] = bot_symbol
            print_board(board)

            if check_winner(board, bot_symbol):
                print("The bot wins. Better luck next time!")
                break

            if is_draw(board):
                print("It's a draw!")
                break

            turn = "Player"


play_game()
