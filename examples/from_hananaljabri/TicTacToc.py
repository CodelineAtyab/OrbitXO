import random
def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 5)
    print("\n")
def check_winner(board, symbol):
    # Check rows, columns, diagonals
    for row in board:
        if all(cell == symbol for cell in row):
            return True
    for col in range(3):
        if all(row[col] == symbol for row in board):
            return True
    if all(board[i][i] == symbol for i in range(3)) or all(board[i][2 - i] == symbol for i in range(3)):
        return True
    return False
def is_draw(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)
def get_available_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] not in ['X', 'O']]
def bot_move(board, bot_symbol):
    available = get_available_moves(board)
    return random.choice(available)
def play_game():
    board = [["1", "2", "3"],
             ["4", "5", "6"],
             ["7", "8", "9"]]
    print("Welcome to Tic Tac Toe!")
    player_symbol = input("Choose your symbol (X or O): ").upper()
    while player_symbol not in ["X", "O"]:
        player_symbol = input("Invalid choice. Please choose X or O: ").upper()
    bot_symbol = "O" if player_symbol == "X" else "X"
    turn = "Player" if player_symbol == "X" else "Bot"
    print_board(board)
    while True:
        if turn == "Player":
            move = input("Enter the number of the cell where you want to place your symbol: ")
            if not move.isdigit():
                print("Please enter a number from 1 to 9.")
                continue
            move = int(move)
            if move < 1 or move > 9:
                print("Invalid cell. Please choose between 1 and 9.")
                continue
            row, col = (move - 1) // 3, (move - 1) % 3
            if board[row][col] in ["X", "O"]:
                print("That cell is already taken.")
                continue
            board[row][col] = player_symbol
            print_board(board)
            if check_winner(board, player_symbol):
                print(":tada: Congratulations! You win!")
                break
            elif is_draw(board):
                print("It's a draw!")
                break
            turn = "Bot"
        else:
            print("Bot is making a move...")
            row, col = bot_move(board, bot_symbol)
            board[row][col] = bot_symbol
            print_board(board)
            if check_winner(board, bot_symbol):
                print(":pensive: The bot wins. Better luck next time!")
                break
            elif is_draw(board):
                print("It's a draw!")
                break
            turn = "Player"
if __name__ == "__main__":
    play_game()