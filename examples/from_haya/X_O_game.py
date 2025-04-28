import random

def display_board(board):
    print()
    for row in board:
        print("  " + " | ".join(row))
        print(" -----------")
    print()

def check_winner(board, symbol):
    for row in board:
        if row[0] == symbol and row[1] == symbol and row[2] == symbol:
            return True
    for col in range(3):
        if board[0][col] == symbol and board[1][col] == symbol and board[2][col] == symbol:
            return True
    if board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol:
        return True
    if board[0][2] == symbol and board[1][1] == symbol and board[2][0] == symbol:
        return True
    return False

def check_draw(board):
    for row in board:
        for cell in row:
            if cell != 'X' and cell != 'O':
                return False
    return True

def player_move(board, player_symbol):
    valid = False
    while not valid:
        move = input("Your move (choose a number 1-9): ")
        if move.isdigit():
            move = int(move)
            if move >= 1 and move <= 9:
                row = (move - 1) // 3
                col = (move - 1) % 3
                if board[row][col] != 'X' and board[row][col] != 'O':
                    board[row][col] = player_symbol
                    valid = True
                else:
                    print("That spot's already taken! Choose another one.")
            else:
                print("Invalid input! Choose a number between 1 and 9.")
        else:
            print("Please enter a number.")

def bot_move(board, bot_symbol):
    available_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] != 'X' and board[row][col] != 'O':
                available_moves.append((row, col))
    move = random.choice(available_moves)
    board[move[0]][move[1]] = bot_symbol
    print("Bot's move:")

def main():
    print("Welcome to Tic Tac Toe!")
    player_symbol = input("Choose your symbol (X or O): ").upper()
    if player_symbol != 'X' and player_symbol != 'O':
        player_symbol = 'X'
    bot_symbol = 'O' if player_symbol == 'X' else 'X'

    board = [['1', '2', '3'],
             ['4', '5', '6'],
             ['7', '8', '9']]
    display_board(board)

    if player_symbol == 'X':
        current_turn = 'player'
    else:
        current_turn = 'bot'

    game_over = False

    while game_over == False:
        if current_turn == 'player':
            player_move(board, player_symbol)
            display_board(board)
            if check_winner(board, player_symbol):
                print("Congratulations! You win!")
                game_over = True
            elif check_draw(board):
                print("It's a draw!")
                game_over = True
            else:
                current_turn = 'bot'
        elif current_turn == 'bot':
            bot_move(board, bot_symbol)
            display_board(board)
            if check_winner(board, bot_symbol):
                print("Bot wins! Better luck next time.")
                game_over = True
            elif check_draw(board):
                print("It's a draw!")
                game_over = True
            else:
                current_turn = 'player'

if __name__ == "__main__":
    main()
