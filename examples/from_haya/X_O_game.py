import random

def display_board(board):
    print()
    print(f'  {board[0]} | {board[1]} | {board[2]}')
    print(' -----------')
    print(f'  {board[3]} | {board[4]} | {board[5]}')
    print(' -----------')
    print(f'  {board[6]} | {board[7]} | {board[8]}')
    print()

def check_winner(board, symbol):
    # Check rows, columns, and diagonals
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    return any(board[a] == board[b] == board[c] == symbol for a, b, c in win_conditions)

def check_draw(board):
    return all(space in ['X', 'O'] for space in board)

def player_move(board, player_symbol):
    while True:
        try:
            move = int(input("Your move (choose a number 1-9): "))
            if move < 1 or move > 9:
                print("Invalid input! Choose a number between 1 and 9.")
                continue
            if board[move - 1] in ['X', 'O']:
                print("That spot's already taken! Choose another one.")
                continue
            board[move - 1] = player_symbol
            break
        except ValueError:
            print("Please enter a valid number.")

def bot_move(board, bot_symbol):
    available_moves = [i for i in range(9) if board[i] not in ['X', 'O']]
    move = random.choice(available_moves)
    board[move] = bot_symbol
    print("Bot's move:")
    
def main():
    print("Welcome to Tic Tac Toe!")
    while True:
        player_symbol = input("Choose your symbol (X or O): ").upper()
        if player_symbol in ['X', 'O']:
            break
        else:
            print("Invalid choice! Please choose X or O.")

    bot_symbol = 'O' if player_symbol == 'X' else 'X'
    print(f"\nYou are {player_symbol}, the bot is {bot_symbol}. Let’s start!")

    board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    display_board(board)

    current_turn = 'player' if player_symbol == 'X' else 'bot'

    while True:
        if current_turn == 'player':
            player_move(board, player_symbol)
            display_board(board)
            if check_winner(board, player_symbol):
                print("Congratulations! You win!")
                break
            elif check_draw(board):
                print("It's a draw!")
                break
            current_turn = 'bot'
        else:
            bot_move(board, bot_symbol)
            display_board(board)
            if check_winner(board, bot_symbol):
                print("Bot wins! Better luck next time.")
                break
            elif check_draw(board):
                print("It's a draw!")
                break
            current_turn = 'player'

if __name__ == "__main__":
    main()
