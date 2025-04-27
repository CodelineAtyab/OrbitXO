f print_board(board):
    print()
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print()
def check_winner(board, symbol):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  
        [0, 4, 8], [2, 4, 6]              
    ]
    for condition in win_conditions:
        if all(board[i] == symbol for i in condition):
            return True
    return False
def player_move(board, player_symbol):
    while True:
        try:
            move = int(input("Your move (choose a number): "))
            if board[move - 1] not in ['X', 'O']:
                board[move - 1] = player_symbol
                break
            else:
                print("Spot already taken. Choose another one.")
        except (IndexError, ValueError):
            print("Invalid input. Please choose a number between 1 and 9.")
def bot_move(board, bot_symbol):
    available_moves = [i for i, spot in enumerate(board) if spot not in ['X', 'O']]
    move = random.choice(available_moves)
    board[move] = bot_symbol
    print(f"Bot chose position {move + 1}")
def is_draw(board):
    return all(spot in ['X', 'O'] for spot in board)
def main():
    board = [str(i) for i in range(1, 10)]
    print("Welcome to Tic Tac Toe!")
    player_symbol = input("Choose your symbol (X or O): ").upper()
    while player_symbol not in ['X', 'O']:
        player_symbol = input("Invalid choice. Please choose X or O: ").upper()
    bot_symbol = 'O' if player_symbol == 'X' else 'X'
    print(f"You are {player_symbol}, the bot is {bot_symbol}. Let's start!")
    print_board(board)
    while True:
        # Player move
        player_move(board, player_symbol)
        print_board(board)
        if check_winner(board, player_symbol):
            print("Congratulations! You win!")
            break
        if is_draw(board):
            print("It's a draw!")
            break
        # Bot move
        bot_move(board, bot_symbol)
        print_board(board)
        if check_winner(board, bot_symbol):
            print("Bot wins! Better luck next time.")
            break
        if is_draw(board):
            print("It's a draw!")
            break
if __name__ == "__main__":
    main()