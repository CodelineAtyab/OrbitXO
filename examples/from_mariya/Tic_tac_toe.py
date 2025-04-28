import random
def print_board(board):
    print()
    print(board[0], '|', board[1], '|', board[2])
    print('--|---|--')
    print(board[3], '|', board[4], '|', board[5])
    print('--|---|--')
    print(board[6], '|', board[7], '|', board[8])
    print()
def check_winner(board, symbol):
    # Check rows
    if board[0] == symbol and board[1] == symbol and board[2] == symbol:
        return True
    elif board[3] == symbol and board[4] == symbol and board[5] == symbol:
        return True
    elif board[6] == symbol and board[7] == symbol and board[8] == symbol:
        return True
    # Check columns
    elif board[0] == symbol and board[3] == symbol and board[6] == symbol:
        return True
    elif board[1] == symbol and board[4] == symbol and board[7] == symbol:
        return True
    elif board[2] == symbol and board[5] == symbol and board[8] == symbol:
        return True
    # Check diagonals
    elif board[0] == symbol and board[4] == symbol and board[8] == symbol:
        return True
    elif board[2] == symbol and board[4] == symbol and board[6] == symbol:
        return True
    else:
        return False
def is_draw(board):
    for spot in board:
        if spot != 'X' and spot != 'O':
            return False  # Still empty spots, so not a draw
    return True  # No empty spots, so it's a draw
def player_move(board, symbol):
    while True:
        move = input("Enter your move (1-9): ")
        if move.isdigit():
            move = int(move) - 1
            if move >= 0 and move <= 8:
                if board[move] != 'X' and board[move] != 'O':
                    board[move] = symbol
                    break
                else:
                    print("Spot already taken! Choose another one.")
            else:
                print("Invalid number! Pick between 1 and 9.")
        else:
            print("Please enter a valid number!")
def bot_move(board, symbol):
    empty_spots = []
    for i in range(9):
        if board[i] != 'X' and board[i] != 'O':
            empty_spots.append(i)
    move = random.choice(empty_spots)
    board[move] = symbol
    print(f"Bot chose spot {move + 1}.")
def main():
    print("Welcome to Tic Tac Toe!")
    while True:
        player_symbol = input("Choose X or O: ").upper()
        if player_symbol == 'X' or player_symbol == 'O':
            break
        else:
            print("Invalid choice. Please choose X or O.")
    if player_symbol == 'X':
        bot_symbol = 'O'
    else:
        bot_symbol = 'X'
    board = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    turn = 'player'
    print_board(board)
    while True:
        if turn == 'player':
            player_move(board, player_symbol)
            print_board(board)
            if check_winner(board, player_symbol):
                print("You win! Congratulations!")
                break
            elif is_draw(board):
                print("It's a draw!")
                break
            else:
                turn = 'bot'
        elif turn == 'bot':
            bot_move(board, bot_symbol)
            print_board(board)
            if check_winner(board, bot_symbol):
                print("Bot wins! Better luck next time.")
                break
            elif is_draw(board):
                print("It's a draw!")
                break
            else:
                turn = 'player'
# Start the game
main()