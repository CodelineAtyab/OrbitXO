import random

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def check_win(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player, player, player] in win_conditions

def is_full(board):
    return all(cell != " " for row in board for cell in row)

def get_bot_move(board, bot_player):
    opponent = "X" if bot_player == "O" else "O"
    
    # 1. Try to win
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = bot_player
                if check_win(board, bot_player):
                    board[i][j] = " "  # Undo move after checking
                    return (i, j)
                board[i][j] = " "  # Undo move after checking

    # 2. Block opponent's winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = opponent
                if check_win(board, opponent):
                    board[i][j] = " "  # Undo move after checking
                    return (i, j)
                board[i][j] = " "  # Undo move after checking

    # 3. Otherwise, pick a random move
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    return random.choice(empty_cells)


def main():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    bot_player = "O"

    while True:
        print_board(board)
        print(f"Player {current_player}'s turn")

        if current_player == "X":
            # Human move
            valid_input = False
            while not valid_input:
                row_input = input("Enter row (0, 1, or 2): ")
                col_input = input("Enter column (0, 1, or 2): ")
                
                if not (row_input.isdigit() and col_input.isdigit()):
                    print("Invalid input. Please enter numbers only.")
                    continue

                row = int(row_input)
                col = int(col_input)

                if not (0 <= row <= 2 and 0 <= col <= 2):
                    print("Invalid input. Numbers must be between 0 and 2.")
                    continue

                if board[row][col] != " ":
                    print("Cell already taken. Try again.")
                    continue

                valid_input = True

        else:
            # Bot move
            row, col = get_bot_move(board, bot_player)
            print(f"Bot chooses: Row {row}, Column {col}")

        board[row][col] = current_player

        if check_win(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main()
