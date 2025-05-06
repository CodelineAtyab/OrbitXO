import random

def print_board(board):
    print("\n")
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print("--+---+--")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print("--+---+--")
    print(f"{board[6]} | {board[7]} | {board[8]}")
    print("\n")

def check_winner(board, symbol):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    return any(all(board[i] == symbol for i in cond) for cond in win_conditions)

def is_draw(board):
    return all(cell != ' ' for cell in board)

def player_move(board, symbol):
    while True:
        try:
            move = int(input(f"Enter your move (1-9): ")) - 1
            if 0 <= move < 9 and board[move] == ' ':
                board[move] = symbol
                break
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Enter a number from 1 to 9.")

def bot_move(board, symbol):
    available = [i for i, cell in enumerate(board) if cell == ' ']
    move = random.choice(available)
    print(f"Bot chooses position {move + 1}")
    board[move] = symbol

def main():
    board = [' '] * 9
    print("Welcome to Tic Tac Toe!")
    player_symbol = ''
    
    while player_symbol not in ['X', 'O']:
        player_symbol = input("Choose your symbol (X or O): ").upper()
    
    bot_symbol = 'O' if player_symbol == 'X' else 'X'
    
    current_turn = 'player' if random.choice([True, False]) else 'bot'
    print(f"{current_turn.capitalize()} goes first!")

    game_over = False

    while not game_over:
        print_board(board)
        
        if current_turn == 'player':
            player_move(board, player_symbol)
            if check_winner(board, player_symbol):
                print_board(board)
                print("🎉 You win!")
                game_over = True
            else:
                current_turn = 'bot'
        else:
            bot_move(board, bot_symbol)
            if check_winner(board, bot_symbol):
                print_board(board)
                print("😔 Bot wins!")
                game_over = True
            else:
                current_turn = 'player'
        
        if not game_over and is_draw(board):
            print_board(board)
            print("🤝 It's a draw!")
            game_over = True

if __name__ == "__main__":
    main()
