import random

def print_board(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
    print("\n")

def check_winner(board, symbol):
    # Check rows, columns, and diagonals
    for i in range(3):
        if all([cell == symbol for cell in board[i]]):  # Row
            return True
        if all([board[j][i] == symbol for j in range(3)]):  # Column
            return True
    if all([board[i][i] == symbol for i in range(3)]):  # Main diagonal
        return True
    if all([board[i][2 - i] == symbol for i in range(3)]):  # Anti-diagonal
        return True
    return False

def is_draw(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)

def get_valid_moves(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] not in ['X', 'O']]

def bot_move(board, bot_symbol):
    valid_moves = get_valid_moves(board)
    return random.choice(valid_moves)

def main():
    board = [[str(i * 3 + j + 1) for j in range(3)] for i in range(3)]

    print("Welcome to Tic Tac Toe!")
    player_symbol = input("Choose your symbol (X or O): ").upper()
    while player_symbol not in ['X', 'O']:
        player_symbol = input("Invalid choice. Choose X or O: ").upper()
    bot_symbol = 'O' if player_symbol == 'X' else 'X'

    current_turn = 'player' if player_symbol == 'X' else 'bot'

    print_board(board)

    while True:
        if current_turn == 'player':
            move = input("Enter your move (1-9): ")
            if not move.isdigit() or not (1 <= int(move) <= 9):
                print("Invalid input. Please enter a number between 1 and 9.")
                continue
            row, col = divmod(int(move) - 1, 3)
            if board[row][col] in ['X', 'O']:
                print("Spot already taken. Choose another.")
                continue
            board[row][col] = player_symbol
            print_board(board)
            if check_winner(board, player_symbol):
                print("You win! 🎉")
                break
            current_turn = 'bot'
        else:
            row, col = bot_move(board, bot_symbol)
            print(f"Bot chooses: {(row * 3 + col + 1)}")
            board[row][col] = bot_symbol
            print_board(board)
            if check_winner(board, bot_symbol):
                print("Bot wins! 🤖")
                break
            current_turn = 'player'

        if is_draw(board):
            print("It's a draw! 😐")
            break

if __name__ == "__main__":
    main()
