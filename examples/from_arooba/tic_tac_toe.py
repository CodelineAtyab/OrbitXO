import random

def print_board(board):
    print()
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("---|---|---")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("---|---|---")
    print(f" {board[6]} | {board[7]} | {board[8]}")
    print()

def check_winner(board, symbol):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8], # horizontal
        [0,3,6], [1,4,7], [2,5,8], # vertical
        [0,4,8], [2,4,6]           # diagonal
    ]
    return any(all(board[i] == symbol for i in condition) for condition in win_conditions)

def is_draw(board):
    return all(spot in ['X', 'O'] for spot in board)

def player_move(board, symbol):
    while True:
        
            move = int(input("Your move (choose a number): ")) - 1
            if move < 0 or move > 8:
                print("Invalid number! Choose 1-9.")
            elif board[move] in ['X', 'O']:
                print("Spot already taken! Choose another.")
            else:
                board[move] = symbol
                break

def bot_move(board, symbol):
    available_moves = [i for i, spot in enumerate(board) if spot not in ['X', 'O']]
    move = random.choice(available_moves)
    board[move] = symbol
    print("Bot's move:")

def main():
    print("Welcome to Tic Tac Toe!")
    while True:
        player_symbol = input("Choose your symbol (X or O): ").upper()
        if player_symbol in ['X', 'O']:
            break
        print("Invalid choice! Please choose X or O.")
    
    bot_symbol = 'O' if player_symbol == 'X' else 'X'
    print(f"You are {player_symbol}, the bot is {bot_symbol}. Let's start!")
    
    board = [str(i) for i in range(1, 10)]
    current_turn = 'player' if player_symbol == 'X' else 'bot'
    
    print_board(board)
    
    while True:
        if current_turn == 'player':
            player_move(board, player_symbol)
            print_board(board)
            if check_winner(board, player_symbol):
                print("Congratulations! You win!")
                break
            current_turn = 'bot'
        else:
            bot_move(board, bot_symbol)
            print_board(board)
            if check_winner(board, bot_symbol):
                print("Bot wins! Better luck next time!")
                break
            current_turn = 'player'
        
        if is_draw(board):
            print("It's a draw!")
            break

if __name__ == "__main__":
    main()
